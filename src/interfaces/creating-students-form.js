function main() 
{
  deleteEverything();

  // Get the data from the responses of supervisors-form-1
  const url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSq4ojmQailO4VAXs61pXaO8aTic2FTDLEuwKHrm5KHcShkkmxriqSDZwn9UNDwSgYvXNypWCh_SNJH/pub?output=csv';
  var csv_content = readDataFromResponses(url);

  // Process the data to get two lists of supervisors, one for bachelor students and the other for master students
  var [list_supervisors_bachelor, list_supervisors_master] = dataProcessing(csv_content);

  // Open up the form
  var form = FormApp.getActiveForm();

  // Choose to build which form, bachelor or master by simply change the boolean variable
  // Note: The app scripts are separate for bachelor and master, only change it here so that we only have to track this file.
  buildBachelorForm = true;
  list_supervisors = buildBachelorForm ? list_supervisors_bachelor : list_supervisors_master;

  // Build up the questions
  buildQuestions(form, list_supervisors);
}

function buildQuestions(form, list_supervisors)
{
  // Sort the supervisors, first project-based then group-based
  list_supervisors.sort((a, b) => sorted_key(a) - sorted_key(b));

  // Add the ID question
  var idQuestion = form.addTextItem();
  idQuestion.setTitle('SCIPER').setRequired(true);
  //TODO: Add validation of whole number

  var sectionProjectOne = form.addPageBreakItem().setTitle("Your 1st choice");
  pagesOne = buildQuestionsOfOneChoice(form, list_supervisors, form.getItems().length-1, true);

  var sectionProjectTwo = form.addPageBreakItem().setTitle("Your 2nd choice");
  form.moveItem(sectionProjectTwo.getIndex(), form.getItems().length-1);
  pagesOne.map(function(page){ page.setGoToPage(sectionProjectTwo); });

  pagesTwo = buildQuestionsOfOneChoice(form, list_supervisors, form.getItems().length-1, true); // start index is the total number of projects

  var sectionProjectThree = form.addPageBreakItem().setTitle("Your 3rd choice");
  form.moveItem(sectionProjectThree.getIndex(), form.getItems().length-1);
  pagesTwo.map(function(page){ page.setGoToPage(sectionProjectThree); });

  pagesThree = buildQuestionsOfOneChoice(form, list_supervisors, form.getItems().length-1, true);

  var sectionProjectFour = form.addPageBreakItem().setTitle("Your 4th choice");
  form.moveItem(sectionProjectFour.getIndex(), form.getItems().length-1);
  pagesThree.map(function(page){ page.setGoToPage(sectionProjectFour); });

  pagesFour = buildQuestionsOfOneChoice(form, list_supervisors, form.getItems().length-1, false);

  var sectionProjectFive = form.addPageBreakItem().setTitle("Your 5th choice");
  form.moveItem(sectionProjectFive.getIndex(), form.getItems().length-1);
  pagesFour.map(function(page){ page.setGoToPage(sectionProjectFive); });

  pagesFive = buildQuestionsOfOneChoice(form, list_supervisors, form.getItems().length-1, false);
  
  //Submit form after that (for both bachelor and master)
  pagesFive.map(function(page){ page.setGoToPage(FormApp.PageNavigationType.SUBMIT); });
}

function buildQuestionsOfOneChoice(form, list_supervisors, index, isRequired) 
{
  // Add 1st question: selecting supervisor
  var supervisorSelection = form.addMultipleChoiceItem();
  form.moveItem(supervisorSelection.getIndex(), form.getItems().length-1);

  supervisorSelection.setTitle('Please select a supervisor')
    .setRequired(isRequired);

  // Extract supervisor names into an array
  var supervisorNames = list_supervisors.map
  (function(supervisor) 
  {
    return supervisor.name.toString(); 
  });

  var choices = [];
  var pages = [];
  for (var i = 0; i < supervisorNames.length; i++)
  {
    var sup = supervisorNames[i];

    var page = form.addPageBreakItem().setTitle(sup);
    pages.push(page);

    var choice = supervisorSelection.createChoice(sup, page);
    choices.push(choice);
  }
  supervisorSelection.setChoices(choices);

  var count_proj_based = 0;
  var count_group_based = 0; 

  for (var i = 0; i < list_supervisors.length; i++)
  {
    var sup = list_supervisors[i];

    // Add question of selecting projects for project-based supervisors. 
    if (sup instanceof SupervisorProjectBased)
    {
      count_proj_based ++;
      var projectQuestion = form.addMultipleChoiceItem().setTitle('Please select a project:').setRequired(true);
      
      var projects = sup.projects;
      var projectTitles = projects.map(function(project)
      {
        return project.title.toString();
      });

      projectQuestion.setChoiceValues(projectTitles);

      form.moveItem(projectQuestion.getIndex(), index + count_proj_based * 3 + count_group_based * 2);  
    }
    else
    {
      count_group_based ++;
    }

    // Add question for required courses
    var courses = sup.courses;
    var filteredCourses = courses.filter(function(course){ return !isNaN(course);});

    if (filteredCourses.length !== 0)
    {
      var coursesQuestion = form.addGridItem().setRequired(true);
      coursesQuestion.setTitle('Please provide the grades of the following course(s): ')
      .setRows(filteredCourses.map(element => "MATH-" + element))
      .setColumns(['<4', '4', '4.25', '4.5', '4.75', '5', '5.25', '5.5', '5.75', '6']);

      form.moveItem(coursesQuestion.getIndex(), index + count_proj_based * 3 + 1 + count_group_based * 2);
    }
  }
  return pages;
}

function dataProcessing(csv_content) 
{
  // Parse CSV data into rows
  const rows = Utilities.parseCsv(csv_content);

  let listSupervisorsMaster = [];
  let listSupervisorsBachelor = [];

  for (let i = 1; i < rows.length; i++) // Need to start from the 2nd row, i.e. i=1
  {
      const row = rows[i];

      // Extract data from each row
      const email = row[1];
      const isChair = row[2] === 'Chair';
      const name = isChair ? row[4] : row[5];
      const courses = [parseInt(row[42]), parseInt(row[43]), parseInt(row[44])].filter(x => !isNaN(x));

      if (row[6] === 'project-based') 
      {
          const rangeNumProjects = row[7];
          let numOtherProjects = 0;

          const masterProjects = [];
          const bachelorProjects = [];

          if (rangeNumProjects === '1 ~ 4') {
              bachelorProjects.push(new Project(row[8], row[9], 'Bachelor'));
              numOtherProjects = row[10];
          } else if (rangeNumProjects === '5 ~ 8') {
              bachelorProjects.push(new Project(row[11], row[12], 'Bachelor'));
              bachelorProjects.push(new Project(row[13], row[14], 'Bachelor'));
              numOtherProjects = row[15];
          }

          for (let j = 0; j < parseInt(numOtherProjects); j++) {
              const startCol = 31 - (3 * j);
              const title = row[startCol];
              const description = row[startCol + 1];
              const targetStudents = row[startCol + 2];

              if (targetStudents === 'Master') {
                  masterProjects.push(new Project(title, description, 'Master'));
              } else if (targetStudents === 'Bachelor') {
                  bachelorProjects.push(new Project(title, description, 'Bachelor'));
              }
          }

          const projects = bachelorProjects.concat(masterProjects);
          const numProjects = projects.length;

          const supervisor = new SupervisorProjectBased(email, name, isChair, numProjects, courses, projects);

          if (masterProjects.length !== 0) {
              listSupervisorsMaster.push(new SupervisorProjectBased(email, name, isChair, masterProjects.length, courses, masterProjects));
          }

          if (bachelorProjects.length !== 0) {
              listSupervisorsBachelor.push(new SupervisorProjectBased(email, name, isChair, bachelorProjects.length, courses, bachelorProjects));
          }
      } 
      else 
      {
          const numProjects = parseInt(row[34]);
          const numBachelorProjects = parseInt(row[33 + numProjects]);
          const numMasterProjects = numProjects - numBachelorProjects;

          const supervisor = new SupervisorGroupBased(email, name, isChair, numProjects, courses, numMasterProjects);

          if (numBachelorProjects !== 0) {
              listSupervisorsBachelor.push(supervisor);
          }

          if (numMasterProjects !== 0) {
              listSupervisorsMaster.push(supervisor);
          }
      }
  }
  return [listSupervisorsBachelor, listSupervisorsMaster];
}

function readDataFromResponses(url)
{
  var response = UrlFetchApp.fetch(url);
  var csv_content = response.getContentText();
  return csv_content;
}

// Clean up codes
function deleteEverything()
{
  var form = FormApp.getActiveForm();
  var items = form.getItems();
  for (var i=0; i<items.length; i++) 
  {
    form.deleteItem(0);
  }
}

function sorted_key(sup) 
{
  return sup instanceof SupervisorProjectBased ? 0 : 1;
}

// Dataclasses
function Project(title, description, target_students) 
{
    this.title = title;
    this.description = description;
    this.target_students = target_students;
}

function Supervisor(email, name, is_chair, num_projects, courses) 
{
  this.email = email;
  this.name = name;
  this.is_chair = is_chair;
  this.num_projects = num_projects;
  this.courses = courses;
}

function SupervisorProjectBased(email, name, is_chair, num_projects, courses, projects) 
{
  Supervisor.call(this, email, name, is_chair, num_projects, courses);
  this.projects = projects;
}

SupervisorProjectBased.prototype = Object.create(Supervisor.prototype);

function SupervisorGroupBased(email, name, is_chair, num_projects, courses, num_master_projects) 
{
  Supervisor.call(this, email, name, is_chair, num_projects, courses);
  this.num_master_projects = num_master_projects;
}

SupervisorGroupBased.prototype = Object.create(Supervisor.prototype);