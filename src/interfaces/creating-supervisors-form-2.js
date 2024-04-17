function main()
{
  deleteEverything();
  
  var form = FormApp.getActiveForm();

  // Get the data from the responses of supervisors-form-1
  const urlSupervisorsResponses = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQMBJ__CI_S02nVV7citWOt15oVU21--nOuyHrJi0JnVN2bJqWUg5ElPy3ZY_7adBXfkxfTaHXvojCg/pub?output=csv'
  var csv_content = readDataFromResponses(urlSupervisorsResponses);
  const rows = Utilities.parseCsv(csv_content);

  // Get the list of indices of project-based supervisors
  var indicesProjectBased = [];
  for (let i = 1; i < rows.length; i++) // Need to start from the 2nd row, i.e. i=1
  {
    if (rows[i][6] === 'project-based') 
    {
      indicesProjectBased.push(i);
    }
  }

  // Create the first question: asking for the identity
  var supervisorSelection = form.addMultipleChoiceItem().setTitle('You are from').setRequired(true);

  var supervisorNames = indicesProjectBased.map
  (function(index) 
  {
    const row = rows[index];
    const isChair = row[2] === 'Chair';
    const name = isChair ? row[4] : row[5];
    return name.toString(); 
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

  return indicesProjectBased;
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