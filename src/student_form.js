function readDataFromResponses(url)
{
  var response = UrlFetchApp.fetch(url);
  var csv_content = response.getContentText();
  return csv_content;
}

function processResponses(csv_content)
{
  var data = Utilities.parseCsv(csv_content);

  var list_supervisors = [];
  var list_supervisors_master = [];
  var list_supervisors_bachelor = [];

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var is_chair = row[2] === 'Chair';

    var name = is_chair ? row[row.length - 2] : row[row.length - 1];

    var courses = [row[row.length - 5], row[row.length - 4], row[row.length - 3]]
                  .filter(function(x) { return !isNaN(x); })
                  .map(function(x) { return parseInt(x); });

    var supervisor;

    if (row[4] === "project-based") 
    {
      var num_projects = parseInt(row[6]);

      var projects = [];
      var master_projects = [];
      var bachelor_projects = [];

      var num_master_projects = 0;
      var num_bachelor_projects = 0;

      for (var index = 0; index < 8; index++) 
      {
        var start_col = 30 - index * 3;
        
        var target_students = row[start_col];
        if (target_students != "" && target_students != null) 
        {
          var description = row[start_col - 1];
          var title = row[start_col - 2];
          
          var project = new Project(title, description, target_students);

          projects.push(project); 

          if (target_students === 'Master') 
          {
            num_master_projects++;
            master_projects.push(project);
          } 
          else if (target_students === 'Bachelor') 
          {
            num_bachelor_projects++;
            bachelor_projects.push(project);
          }
        }
      }
      supervisor = new SupervisorProjectBased(name, is_chair, num_projects, courses, projects);

      if (num_master_projects !== 0) 
      {
        list_supervisors_master.push(new SupervisorProjectBased(name, is_chair, num_master_projects, courses, master_projects));
      }

      if (num_bachelor_projects !== 0) 
      {
        list_supervisors_bachelor.push(new SupervisorProjectBased(name, is_chair, num_bachelor_projects, courses, bachelor_projects));
      }
    } 
    else 
    {
      var num_projects = parseInt(row[row.length - 7]);
      var num_master_projects = parseInt(row[row.length - 6]);
      var num_bachelor_projects = num_projects - num_master_projects;
      supervisor = new SupervisorGroupBased(name, is_chair, num_projects, courses, num_master_projects);

      if (num_bachelor_projects !== 0) 
      {
        list_supervisors_bachelor.push(supervisor);
      }
      if (num_master_projects !== 0) 
      {
        list_supervisors_master.push(supervisor);
      }
    }

    list_supervisors.push(supervisor);
  }
  
  return [list_supervisors, list_supervisors_bachelor, list_supervisors_master];
}

function buildQuestionsOfOneChoice(isBachelor, form, list_supervisors, index, masterPage, isRequired) 
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

  if (isBachelor)
  {
    form.moveItem(masterPage.getIndex(), form.getItems().length-1);
  }

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

      if (isBachelor)
      {
        form.moveItem(projectQuestion.getIndex(), index + count_proj_based * 3 - 1 + count_group_based * 2);
      }
      else
      {
        form.moveItem(projectQuestion.getIndex(), index + count_proj_based * 3 - 1 + count_group_based * 2);
      }
      
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
      if (isBachelor)
      {
        form.moveItem(coursesQuestion.getIndex(), index + count_proj_based * 3 + count_group_based * 2);
      }
      else
      {
        form.moveItem(projectQuestion.getIndex(), index + count_proj_based * 3 + count_group_based * 2);
      }
    }
  }

  return pages;
}

function Project(title, description, target_students) {
    this.title = title;
    this.description = description;
    this.target_students = target_students;
}

function Supervisor(name, is_chair, num_projects, courses) {
  this.name = name;
  this.is_chair = is_chair;
  this.num_projects = num_projects;
  this.courses = courses;
}

function SupervisorProjectBased(name, is_chair, num_projects, courses, projects) {
  Supervisor.call(this, name, is_chair, num_projects, courses);
  this.projects = projects;
}

SupervisorProjectBased.prototype = Object.create(Supervisor.prototype);

function SupervisorGroupBased(name, is_chair, num_projects, courses, num_master_projects) {
  Supervisor.call(this, name, is_chair, num_projects, courses);
  this.num_master_projects = num_master_projects;
}

SupervisorGroupBased.prototype = Object.create(Supervisor.prototype);

function main() 
{
  // Clean up the form
  deleteEverything();

  // Get the data from supervisors-form-1
  var url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT2TSn3joZFFrBeGShjgUHeTm5Zw1v3vPhxl53Wht0OVXDWAOtnZ_JbNrAgakmpJBOThZ00hUG5pyVV/pub?output=csv';
  var csv_content = readDataFromResponses(url);
  var [list_supervisors, list_supervisors_bachelor, list_supervisors_master] = processResponses(csv_content);

  // Open up the form
  var form = FormApp.getActiveForm();

  // Add basic questions
  var idQuestion = form.addTextItem();
  idQuestion.setTitle('SCIPER').setRequired(true);

  var degreeQuestion = form.addMultipleChoiceItem();
  degreeQuestion.setTitle('Degree').setRequired(true);

  var bachelorPage = form.addPageBreakItem().setTitle("Your 1st choice");
  var masterPage = form.addPageBreakItem().setTitle("Your 1st choice");

  var bachelorChoice = degreeQuestion.createChoice("bachelor", bachelorPage);
  var masterChoice = degreeQuestion.createChoice("master", masterPage);

  degreeQuestion.setChoices([bachelorChoice, masterChoice]);

  /*
  Bachelor questions
  */
  buildQuestions(true, form, list_supervisors_bachelor, masterPage);

  /*
  Master questions
  */
  buildQuestions(false, form, list_supervisors_master, masterPage);
}

function buildQuestions(isBachelor, form, list_supervisors, masterPage)
{
  list_supervisors.sort((a, b) => sorted_key(a) - sorted_key(b));
  
  pagesOne = buildQuestionsOfOneChoice(isBachelor, form, list_supervisors, form.getItems().length-1, masterPage, true);

  var sectionProjectTwo = form.addPageBreakItem().setTitle("Your 2nd choice");
  form.moveItem(sectionProjectTwo.getIndex(), form.getItems().length-1);
  pagesOne.map(function(page){ page.setGoToPage(sectionProjectTwo); });

  pagesTwo = buildQuestionsOfOneChoice(isBachelor, form, list_supervisors, form.getItems().length-1, masterPage, true); // start index is the total number of projects

  var sectionProjectThree = form.addPageBreakItem().setTitle("Your 3rd choice");
  form.moveItem(sectionProjectThree.getIndex(), form.getItems().length-1);
  pagesTwo.map(function(page){ page.setGoToPage(sectionProjectThree); });

  pagesThree = buildQuestionsOfOneChoice(isBachelor, form, list_supervisors, form.getItems().length-1, masterPage, true);

  var sectionProjectFour = form.addPageBreakItem().setTitle("Your 4th choice");
  form.moveItem(sectionProjectFour.getIndex(), form.getItems().length-1);
  pagesThree.map(function(page){ page.setGoToPage(sectionProjectFour); });

  pagesFour = buildQuestionsOfOneChoice(isBachelor, form, list_supervisors, form.getItems().length-1, masterPage, false);

  var sectionProjectFive = form.addPageBreakItem().setTitle("Your 5th choice");
  form.moveItem(sectionProjectFive.getIndex(), form.getItems().length-1);
  pagesFour.map(function(page){ page.setGoToPage(sectionProjectFive); });

  pagesFive = buildQuestionsOfOneChoice(isBachelor, form, list_supervisors, form.getItems().length-1, masterPage, false);
  
  //Submit form after that (for both bachelor and master)
  pagesFive.map(function(page){ page.setGoToPage(FormApp.PageNavigationType.SUBMIT); });
}

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
