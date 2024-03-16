/*
This file is the App Script extension of Supervisor-1 (Responses).
Only for storage and version contorl. 
No need to execute it here. 
*/

function readDataFromResponses(url){
    var response = UrlFetchApp.fetch(url);
    var csv_content = response.getContentText();
    return csv_content
  }
  
  function processResponses(csv_content){
    var data = Utilities.parseCsv(csv_content);
    var list_supervisors = [];
  
    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      var is_chair = row[2] === 'Chair';
  
      var name = is_chair ? row[row.length - 2] : row[row.length - 1];
  
      var courses = [row[row.length - 5], row[row.length - 4], row[row.length - 3]]
                    .filter(function(x) { return !isNaN(x); })
                    .map(function(x) { return parseInt(x); });
  
      var supervisor;
  
      if (row[4] === "project-based") {
        var num_projects = parseInt(row[6]);
        var projects = [];
        supervisor = new SupervisorProjectBased(name, is_chair, num_projects, courses, projects);
      } 
      else {
        var num_projects = parseInt(row[row.length - 7]);
        var num_master_projects = parseInt(row[row.length - 6]);
        supervisor = new SupervisorGroupBased(name, is_chair, num_projects, courses, num_master_projects);
      }
  
      list_supervisors.push(supervisor);
  
      return list_supervisors
    }
  }
  
  function createSupervisorSelectionQuestion(list_supervisors) {
    // Assuming list_supervisors is defined and populated in the previous code snippet
    var formId = '1BUrjIpvwT5SQzEAW61qhBTDr0XL5RP1DTRp-kkEjaEo'
    var form = FormApp.openById(formId);
  
    // Add a multiple-choice question
    var item = form.addMultipleChoiceItem();
    item.setTitle('Please select your preferred supervisor for your project:')
      .setRequired(true);
  
    // Populate options from the list_supervisors array
    for (var i = 0; i < list_supervisors.length; i++) {
      var supervisorName = list_supervisors[i].name;
      item.createChoice(supervisorName);
    }
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
  
  function main() {
    var url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT2TSn3joZFFrBeGShjgUHeTm5Zw1v3vPhxl53Wht0OVXDWAOtnZ_JbNrAgakmpJBOThZ00hUG5pyVV/pub?output=csv'
    var csv_content = readDataFromResponses(url)
    createSupervisorSelectionQuestion(csv_content)
  }