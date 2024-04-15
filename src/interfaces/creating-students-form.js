function main() 
{
  deleteEverything();

  // Get the data from the responses of supervisors-form-1
  const url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQMBJ__CI_S02nVV7citWOt15oVU21--nOuyHrJi0JnVN2bJqWUg5ElPy3ZY_7adBXfkxfTaHXvojCg/pub?output=csv';
  var csv_content = readDataFromResponses(url);

  // Process the data to get two lists of supervisors, one for bachelor students and the other for master students
  var [list_supervisors_bachelor, list_supervisors_master] = dataProcessing(csv_content);

  // Open up the form
  var form = FormApp.getActiveForm();

  // Choose to build which form, bachelor or master by simply change the boolean variable
  // Note: The app scripts are separate for bachelor and master, only change it here so that we only have to track this file.
  buildBachelorForm = false;
  list_supervisors = buildBachelorForm ? list_supervisors_bachelor : list_supervisors_master;

  // Build up the questions
  buildQuestions(form, list_supervisors);
}

function buildQuestions(form, list_supervisors)
{
  // Sort the supervisors, first project-based then group-based
  // list_supervisors.sort((a, b) => sorted_key(a) - sorted_key(b));

  // Ask for their names
  var firstNameQuestion = form.addTextItem();
  firstNameQuestion.setTitle('First name').setRequired(true);

  var lastNameQuestion = form.addTextItem();
  lastNameQuestion.setTitle('Last name').setRequired(true);

  // Ask for students' SCIPER
  var idQuestion = form.addTextItem();
  idQuestion.setTitle('SCIPER').setRequired(true);

  // Add Validation for SCIPER input
  var idValidation = FormApp.createTextValidation().requireWholeNumber().build();
  idQuestion.setValidation(idValidation);

  var sectionProjectOne = form.addPageBreakItem().setTitle("Your 1st choice");
  pagesOne = buildQuestionsOfOneChoice(form, list_supervisors, true);

  var sectionProjectTwo = form.addPageBreakItem().setTitle("Your 2nd choice");
  form.moveItem(sectionProjectTwo.getIndex(), form.getItems().length-1);
  pagesOne.map(function(page){ page.setGoToPage(sectionProjectTwo); });

  pagesTwo = buildQuestionsOfOneChoice(form, list_supervisors, true); // start index is the total number of projects

  var sectionProjectThree = form.addPageBreakItem().setTitle("Your 3rd choice");
  form.moveItem(sectionProjectThree.getIndex(), form.getItems().length-1);
  pagesTwo.map(function(page){ page.setGoToPage(sectionProjectThree); });

  pagesThree = buildQuestionsOfOneChoice(form, list_supervisors, true);

  var sectionProjectFour = form.addPageBreakItem().setTitle("Your 4th choice");
  form.moveItem(sectionProjectFour.getIndex(), form.getItems().length-1);
  pagesThree.map(function(page){ page.setGoToPage(sectionProjectFour); });

  pagesFour = buildQuestionsOfOneChoice(form, list_supervisors, false);

  var sectionProjectFive = form.addPageBreakItem().setTitle("Your 5th choice");
  form.moveItem(sectionProjectFive.getIndex(), form.getItems().length-1);
  pagesFour.map(function(page){ page.setGoToPage(sectionProjectFive); });

  pagesFive = buildQuestionsOfOneChoice(form, list_supervisors, false);
  
  //Submit form after that (for both bachelor and master)
  pagesFive.map(function(page){ page.setGoToPage(FormApp.PageNavigationType.SUBMIT); });
}

function buildQuestionsOfOneChoice(form, list_supervisors, isRequired) 
{
  // Add 1st question: selecting supervisor
  var supervisorSelection = form.addMultipleChoiceItem();
  form.moveItem(supervisorSelection.getIndex(), form.getItems().length-1);

  supervisorSelection.setTitle('Please select a supervisor')
    .setRequired(isRequired);

  // Extract supervisor names into an array, together with attribute of project-based/group-based
  var supervisorNames = list_supervisors.map
  (function(supervisor) 
  {
    let sup_type = (supervisor instanceof SupervisorProjectBased) ? '[Project-based] ' : '[Group-based] ';
    return sup_type + supervisor.name.toString(); 
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

  for (var i = 0; i < list_supervisors.length; i++)
  {
    var sup = list_supervisors[i];
    var indexMoveItem = pages[i].getIndex(); // Index of section of this supervisor

    const hasProjectsQuestion = sup instanceof SupervisorProjectBased;

    var courses = sup.courses;
    var filteredCourses = courses.filter(function(course){ return !isNaN(course);});
    const hasCoursesQuestion = filteredCourses.length !== 0;

    // Add question of selecting projects for project-based supervisors. 
    if (hasProjectsQuestion)
    {
      indexMoveItem ++; // Update the index for moving item

      var projectQuestion = form.addMultipleChoiceItem().setTitle('Please select a project:').setRequired(true);
    
      var projectTitles = (sup.projects).map(
        function(project)
        {
          return project.title.toString();
        }
      );

      projectQuestion.setChoiceValues(projectTitles);

      form.moveItem(projectQuestion.getIndex(), indexMoveItem);
    }
    
    // Add question of required courses
    if (hasCoursesQuestion)
    {
      indexMoveItem ++;

      var coursesQuestion = form.addGridItem().setRequired(true);
      coursesQuestion.setTitle('Please provide the grades of the following course(s): ')
      .setRows(filteredCourses.map(element => "MATH-" + element))
      .setColumns(['<4', '4', '4.25', '4.5', '4.75', '5', '5.25', '5.5', '5.75', '6']);

      form.moveItem(coursesQuestion.getIndex(), indexMoveItem);
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
    const courses = [parseInt(row[48]), parseInt(row[49]), parseInt(row[50])].filter(x => !isNaN(x));

    if (row[6] === 'project-based') 
    {
      const rangeNumProjects = row[7];
      let numOtherProjects = 0;

      var supervisor;
      var supervisorBachelor;
      var supervisorMaster;

      const masterProjects = [];
      const bachelorProjects = [];
      const undefinedProjects = [];

      if (rangeNumProjects === '1 ~ 4') 
      {
        bachelorProjects.push(new Project(row[8], row[9], 'bachelor'));
        numOtherProjects = row[10];
      } 
      else if (rangeNumProjects === '5 ~ 8') 
      {
        bachelorProjects.push(new Project(row[11], row[12], 'bachelor'));
        bachelorProjects.push(new Project(row[13], row[14], 'bachelor'));
        numOtherProjects = row[15];
      }

      for (let j = 0; j < parseInt(numOtherProjects); j++) 
      {
        const startCol = 31 - (3 * j);
        const title = row[startCol];
        const description = row[startCol + 1];
        const targetStudents = row[startCol + 2];

        if (targetStudents === 'Master') 
        {
          masterProjects.push(new Project(title, description, 'master'));
        } 
        else if (targetStudents === 'Bachelor') 
        {
          bachelorProjects.push(new Project(title, description, 'bachelor'));
        }
        else
        {
          undefinedProjects.push(new Project(title, description, 'undefined'));
        }
      }

      const projects = [...bachelorProjects, ...masterProjects, ...undefinedProjects];
      const numProjects = projects.length;

      supervisor = new SupervisorProjectBased(email, name, isChair, numProjects, courses, 
      bachelorProjects.length, masterProjects.length, undefinedProjects.length, projects);

      supervisorBachelor = new SupervisorProjectBased(email, name, isChair, numProjects - masterProjects.length, courses, 
      bachelorProjects.length, 0, undefinedProjects.length, bachelorProjects.concat(undefinedProjects));

      supervisorMaster = new SupervisorProjectBased(email, name, isChair, numProjects - bachelorProjects.length, courses, 
      0, masterProjects.length, undefinedProjects.length, masterProjects.concat(undefinedProjects));
    } 
    else 
    {
      const numProjects = parseInt(row[34]);
      const numBachelorProjects = parseInt(row[33 + numProjects]);
      const numMasterProjects = parseInt(row[41 + numProjects - numBachelorProjects]);
      const numUndefinedProjects = numProjects - numBachelorProjects - numMasterProjects;

      supervisor = new SupervisorGroupBased(email, name, isChair, numProjects, courses,
      numBachelorProjects, numMasterProjects, numUndefinedProjects);

      supervisorBachelor = new SupervisorGroupBased(email, name, isChair, numProjects - numMasterProjects, courses,
      numBachelorProjects, 0, numUndefinedProjects);

      supervisorMaster = new SupervisorGroupBased(email, name, isChair, numProjects - numBachelorProjects, courses, 
      0, numMasterProjects, numUndefinedProjects);
    }

    if ((supervisor.num_bachelor_projects + supervisor.num_undefined_projects) !== 0) 
    {
      listSupervisorsBachelor.push(supervisorBachelor);
    }

    if ((supervisor.num_master_projects + supervisor.num_undefined_projects) !== 0) 
    {
      listSupervisorsMaster.push(supervisorMaster);
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

// function sorted_key(sup) 
// {
//   return sup instanceof SupervisorProjectBased ? 0 : 1;
// }

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

function SupervisorProjectBased(email, name, is_chair, num_projects, courses, num_bachelor_projects, num_master_projects, num_undefined_projects, projects) 
{
  Supervisor.call(this, email, name, is_chair, num_projects, courses);

  this.num_bachelor_projects = num_bachelor_projects;
  this.num_master_projects = num_master_projects;
  this.num_undefined_projects = num_undefined_projects;

  this.projects = projects;
}

SupervisorProjectBased.prototype = Object.create(Supervisor.prototype);

function SupervisorGroupBased(email, name, is_chair, num_projects, courses, num_bachelor_projects, num_master_projects, num_undefined_projects) 
{
  Supervisor.call(this, email, name, is_chair, num_projects, courses);

  this.num_bachelor_projects = num_bachelor_projects;
  this.num_master_projects = num_master_projects;
  this.num_undefined_projects = num_undefined_projects;
}

SupervisorGroupBased.prototype = Object.create(Supervisor.prototype);