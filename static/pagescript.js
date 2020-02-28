
class LoadedArticle {
    constructor() {
      this.sentenceConstruction = [];
      this.name = "";
      this.sentence = "";
      this.neuralMatchType = "grammar"
      this.neuralMatchLength = "full"
      this.results = []
    }
    addResult(data)
    {
      this.results.push(data)
      displayPatternResults()
    }
  }
  
  let currentArt = new LoadedArticle();
  
  function seperateTextBySentences(text)
  {
      var result = text.match( /[^\.!\?]+[\.!\?]+/g );
      return result
  }
  
  function removePatternResult(indx)
  {
      currentArt.results.splice(indx, 1); 
      displayPatternResults()
  }
  
  function displayPatternResults()
  {
      data = currentArt.results
      var r = document.getElementById("finalResultSpan");
      removeChildren(r)
  
      var listElement = document.createElement('ol')
      r.appendChild(listElement)
  
      for (let x in data)
      {
          var anchor = document.createElement("li");
          var inner = document.createElement('ul');
          anchor.appendChild(inner);
          for (y in data[x])
          {
              var subItem = document.createElement('li')
              subItem.innerHTML = data[x][y];
              inner.appendChild(subItem);
          }
          
          var btnWhole0 = document.createElement("button");
          btnWhole0.innerHTML = "Remove";
  
          btnWhole0.addEventListener("click", function()
          {
              removePatternResult(x);
          });
          anchor.appendChild(btnWhole0);
          listElement.appendChild(anchor);
      }
  
  }
  
  function showHandReturn(data)
  {
  
      //currentArt.addResult(["Hand",data[3],data[4]])
      var wordArr = "";
      var grammarArr = "";
      for (x in data)
      {
          innerArr = data[x].split(',');
          wordArr+=innerArr[0]+" ";
          grammarArr+=innerArr[1]+" ";
      }
      currentArt.addResult(['Added by Hand',wordArr,grammarArr]);
      //showReturnResult(data,"Hand");
  }
  
  function confirmRegexPattern(data)
  {
      currentArt.addResult(['Added by Regex',data['Matching'],data['Regex Matched']])
  }
  
  function showRegexReturn(data)
  {
      showReturnRegexResult(data,"Regex")
      //currentArt.addResult(["Regex",data[3],data[4]])
  }
  
  function confirmNeuralPattern(data)
  {
      currentArt.addResult(["Added by Neural",data['Article Text'],data['Article Grammar']])
  }
  
  function showNeuralReturn(data)
  {
      showReturnResult(data,"Neural")
  }
  
  function showReturnRegexResult(data,type)
  {
      var q = document.getElementById("questionResultSpan");
      removeChildren(q)
      var listContainer = document.createElement('div')
      var listElement = document.createElement('ol')
      listContainer.appendChild(listElement)
      var isItem = false
      for (let x in data) 
      {
          var isValue = true
          
          for (let y in data[x]) 
          {   
              var innerItem = document.createElement('li')
              var listItem = document.createElement('ol')
  
              if (data[x][y] ==false)
              {
                  isValue = false
              }
              for (let [key, value] of Object.entries(data[x][y])) 
              {
                  var subItem = document.createElement('li')
                  subItem.innerHTML = `${key}: ${value}`;
                  listItem.appendChild(subItem)
              }
  
              if (isValue != false)
              {
                  isItem = true
                  listElement.appendChild(innerItem)
                  var btnWhole0 = document.createElement("button");
                  btnWhole0.innerHTML = "Add result";
                  if (type == "Regex")
                  {
                      btnWhole0.addEventListener("click", function()
                      {
                          confirmRegexPattern(data[x][y])
                      });
                  }
                  
                  innerItem.appendChild(listItem)
                  innerItem.appendChild(btnWhole0)
              }
          }
      }
  
      if (!isItem)
      {
          var anchor = document.createElement("a");
          anchor.innerHTML = "No Regex Matches";
          listContainer.appendChild(anchor)
      }
  
      q.appendChild(listContainer)
  }
  
  function showReturnResult(data,type)
  {
      var q = document.getElementById("questionResultSpan");
      removeChildren(q)
      var listContainer = document.createElement('div')
      var listElement = document.createElement('ol')
      listContainer.appendChild(listElement)
      for (let x in data) 
      {
          var innerItem = document.createElement('li')
          listElement.appendChild(innerItem)
          var listItem = document.createElement('ul')
          for (let [key, value] of Object.entries(data[x])) 
          {
              var subItem = document.createElement('li')
              subItem.innerHTML = `${key}: ${value}`;
              listItem.appendChild(subItem)
  
          }
          var btnWhole0 = document.createElement("button");
          btnWhole0.innerHTML = "Add result";
          if (type == "Neural")
          {
              btnWhole0.addEventListener("click", function()
              {
                  confirmNeuralPattern(data[x])
              });
          }
          else if (type == "Regex")
          {
              btnWhole0.addEventListener("click", function()
              {
                  confirmRegexPattern(data[x])
              });
          }
          else if (type == "Hand")
          {
              btnWhole0.addEventListener("click", function()
              {
                  confirmHandPattern(data[x])
              });
          }
          innerItem.appendChild(listItem)
          innerItem.appendChild(btnWhole0)
      }
      q.appendChild(listContainer)
  }
  
  function checkRegexPatterns()
  {
      $.getJSON($SCRIPT_ROOT + '/ajaxReturnPatterns',
                  {
                  valArticle: currentArt.name
                  },
                  function(data) 
                  {
                      showRegexReturn(data.result);
                  });
  }
  
  function checkNeuralPatterns()
  {
      $.getJSON($SCRIPT_ROOT + '/ajaxneuralmatches',
                  {
                      valMatchGrammar: currentArt.neuralMatchType,
                      valMatchLength: currentArt.neuralMatchLength
                  },
                  function(data) 
                  {
                      showNeuralReturn(data.result)
                      
                  });
  }
  
  function getArticlePatterns(articleName)
  {
      $.getJSON($SCRIPT_ROOT + '/ajaxReturnPatterns',
                  {async: false,
                  valArticleName: articleName
                  },
                  function(data) 
                  {
                      //splitSentence(data.result);
                  });
  }
  
  function getStructure(section,sentence)
  {
      $.ajax({
              url: $SCRIPT_ROOT + '/ajaxAnalyzeRegex',
              data: { valSentenceToAnalyze: sentence,
                      valSectionToAnalyze: section
                      },
                  traditional: true,
              success: function(data) 
              {
                  splitSentence(data.result1,data.result0,data.graph);
              }
              });
      /*$.getJSON($SCRIPT_ROOT + '/ajaxAnalyzeRegex',
                  {async: false,
                  valSentenceToAnalyze: sentence
                  },
                  function(data) 
                  {
                      splitSentence(section, data.result);
                  });*/
  }
  
  function displaySentence(sentence)
  {
      var sen = document.getElementById("selectedSentence");
      removeChildren(sen);
      var anchor = document.createElement("a");
      anchor.innerHTML = sentence;
      sen.appendChild(anchor);
  }
  
  function removeChildren(element)
  {
      while (element.firstChild) 
      {
          element.removeChild(element.firstChild);
      }
  }
  
  function resetConstructionImage()
  {
      var sen = document.getElementById("constructedSentence");
      removeChildren(sen);
      var sen1 = document.getElementById("constructedGrammar");
      removeChildren(sen1);
  }
  function resetConstruction()
  {
      currentArt.sentenceConstruction = [];
      resetConstructionImage();
      
  }
  
  function updateConstruction(c)
  {
      resetConstructionImage();
      var sen0 = document.getElementById("constructedSentence");
      var sen1 = document.getElementById("constructedGrammar");
      for (let i in c)
      {               
          var btn0 = document.createElement("button");
              btn0.innerHTML = c[i][0];
              btn0.className = "fixedbtn";
          var btn1 = document.createElement("button");
              btn1.innerHTML = c[i][1];
              btn1.className = "fixedbtn";
          sen0.appendChild(btn0);
          sen1.appendChild(btn1);
      }
  }
  
  function addWholeConstruction(sentence)
  {
      for(let i in sentence)
      {
          addWordToConstruction(sentence[i][0],sentence[i][1])
      }
  }
  
  function addWordToConstruction(word,grammar,index)
  {
      currentArt.sentenceConstruction.push([word,grammar,index]);
      updateConstruction(currentArt.sentenceConstruction);
  }
  
  function getColumn(array,col)
  {
      temp = []
      for (var x in array)
      {
          temp.push(array[x][col])
      }
      return temp
  }
  
  function arrayToString(arr)
  {
      temp = []
      for (var x in arr)
      {
          temp.push(arr[x])
      }
      return temp
  }
  
  function saveRegexPattern()
  {
      var sendP = currentArt.sentenceConstruction;
      var sendS = currentArt.sentence;
  
      $.ajax({
              url: $SCRIPT_ROOT + '/ajaxSavePattern',
              data: { valPattern: sendP,
                      valSentence: sendS,
                      valSaveType: "Regex" 
                      },
                  traditional: true,
              success: function(data) 
              {
                  //showHandReturn(data.result)
              }
              });
  }
  
  function saveNeuralPattern()
  {
      var sendP = currentArt.sentenceConstruction;
      var sendS = currentArt.sentence;
      $.ajax({
      url: $SCRIPT_ROOT + '/ajaxSavePattern',
      data: { valPattern: sendP,
              valSentence: sendS,
              valSaveType: "Neural" 
              },
      traditional: true,
      success: function(data) 
      {
          //showHandReturn(data.result)
      }
  });
  }
  
  function savePattern()
  {
      var sendP = currentArt.sentenceConstruction;
      var sendS = currentArt.sentence;
      $.ajax({
      url: $SCRIPT_ROOT + '/ajaxSavePattern',
      data: { valPattern: sendP,
              valSentence: sendS,
              valSaveType: "Show" 
              },
      traditional: true,
      success: function(data) 
      {
          showHandReturn(data.result)
      }
  });
  }
  
  function makeGraph(place,graph)
  {
      var sec0 = document.getElementById("selectedSentence");
  }
  
  function splitSentence(section,sentence,graph)
  {
      currentArt.sentence = sentence
      var sen0 = document.getElementById("selectedSentence");
      removeChildren(sen0);
      var sen1 = document.getElementById("selectedGrammar");
      removeChildren(sen1);
      var sen2 = document.getElementById("otherButtons");
      removeChildren(sen2);
  
      var sen3 = document.getElementById("selectedSectionText");
      removeChildren(sen3);
  
      var sen4 = document.getElementById("selectedSectionGrammar");
      removeChildren(sen4);
  
      var anchorSectionText = document.createElement("a");
      var anchorSectionGrammar = document.createElement("a");
      var anchor = document.createElement("a");
      var anchor1 = document.createElement("a");
  
      var btnWhole0 = document.createElement("button");
          btnWhole0.innerHTML = "Add All Words";
          btnWhole0.addEventListener("click", function()
          {
              addWholeConstruction(sentence)
          });
      
      var btnWhole1 = document.createElement("button");
          btnWhole1.innerHTML = "Add Neural Pattern";
          btnWhole1.addEventListener("click", function()
          {
              saveNeuralPattern()
          });
  
      var btnWhole2 = document.createElement("button");
      btnWhole2.innerHTML = "Add Regex Pattern";
      btnWhole2.addEventListener("click", function()
      {
          saveRegexPattern()
      });
  
      var btnWhole3 = document.createElement("button");
      btnWhole3.innerHTML = "Show Pattern";
      btnWhole3.addEventListener("click", function()
      {
          savePattern()
      });
      
      sen2.appendChild(btnWhole0);
      sen2.appendChild(btnWhole1);
      sen2.appendChild(btnWhole2);
      sen2.appendChild(btnWhole3);
  
      console.log(section)
      for (let i in section)
      {
          for (let i1 in section[i])
          {
              let val0 = section[i][i1][0];
              let val1 = section[i][i1][1];
  
              var btnSec0 = document.createElement("button");
              btnSec0.innerHTML = section[i][i1][0];
              btnSec0.className = "fixedbtn";   
              btnSec0.addEventListener("click", function()
              {
                  addWordToConstruction(val0,val1,i)
              }); 
              anchorSectionText.appendChild(btnSec0);
  
              var btnSec1 = document.createElement("button");
              btnSec1.innerHTML = section[i][i1][1];
              btnSec1.className = "fixedbtn";   
              btnSec1.addEventListener("click", function()
              {
                  addWordToConstruction(val0,val1,i)
              }); 
              anchorSectionGrammar.appendChild(btnSec1);
  
          }
      }
  
      for (let i in sentence) 
      {
          let val0 = sentence[i][0];
          let val1 = sentence[i][1];
          var btn = document.createElement("button");
          btn.innerHTML = val0;
          btn.className = "fixedbtn";   
          anchor.appendChild(btn);
          var btn2 = document.createElement("button");
          btn2.className = "fixedbtn";
          btn2.innerHTML = val1;
          anchor1.appendChild(btn2);
          btn.addEventListener("click", function()
          {
              addWordToConstruction(val0,val1,i)
          }); 
  
          btn2.addEventListener("click", function()
          {
              addWordToConstruction(val0,val1,i)
          }); 
  
      }
      sen0.appendChild(anchor);
      sen1.appendChild(anchor1);
      sen3.appendChild(anchorSectionText);
      sen4.appendChild(anchorSectionGrammar);
  }
  
  function selectSentence(section,sentence)
  {
      getStructure(section,sentence);
  }
  
  function displayPatternMatches(result)
  {
  
  }
  
  function addDocumentButtons()
  {
      var patternButtonSpan = document.getElementById("checkPatternSpan");
      removeChildren(patternButtonSpan);
      var btnPattern = document.createElement("button");
          btnPattern.innerHTML = "Check Regex Patterns";
          btnPattern.addEventListener("click", function()
          {
              checkRegexPatterns();
          }); 
      patternButtonSpan.appendChild(btnPattern);
  
      var patternButtonNeuralSpan = document.getElementById("checkPatternNeuralSpan");
      removeChildren(patternButtonNeuralSpan);
      var btnPattern1 = document.createElement("button");
          btnPattern1.innerHTML = "Check Neural Patterns";
          btnPattern1.addEventListener("click", function()
          {
              checkNeuralPatterns();
          }); 
      patternButtonNeuralSpan.appendChild(btnPattern1);
      ////////
      var select = document.createElement("select");
      select.id = "neuralSelect";
      select.name="neuralSelect";
  
      var option0 = document.createElement("option");
      option0.value=0;
      option0.selected="";
      option0.innerHTML= "grammar";
      option0.addEventListener("click", function()
      {
          currentArt.neuralMatchType = "grammar"
      }); 
  
      var option1 = document.createElement("option");
      option1.value=1;
      option1.innerHTML= "text";
      option1.addEventListener("click", function()
      {
          currentArt.neuralMatchType = "text"
      }); 
  
      select.appendChild(option0);
      select.appendChild(option1);
      /////////
      var select1 = document.createElement("select");
      select1.id = "neuralLength";
      select1.name="neuralLength";
  
      var option2 = document.createElement("option");
      option2.value=0;
      option2.selected="";
      option2.innerHTML= "long";
      option2.addEventListener("click", function()
      {
          currentArt.neuralMatchLength = "long"
      }); 
  
      var option3 = document.createElement("option");
      option3.value=1;
      option3.innerHTML= "short";
      option3.addEventListener("click", function()
      {
          currentArt.neuralMatchLength = "short"
      }); 
      ///
      select1.appendChild(option2);
      select1.appendChild(option3);
  
      patternButtonNeuralSpan.appendChild(select);
      patternButtonNeuralSpan.appendChild(select1);
  }
  
  function displayDocument(result)
  {
      currentArt.name = result[0]
      strs = result[1]
  
      addDocumentButtons()
      
      var listHold = document.getElementById("listAnchor");
      removeChildren(listHold);
      
      var list = document.createElement("ol");
      listHold.appendChild(list);
      //console.log(strs);
      for (let i in strs) 
      {
          for (let j in strs[i].Text)
          {
              var innerItem = document.createElement('li')
              var anchor = document.createElement("a");
              anchor.href = "#";
              let t0 = strs[i].Title;
              let t1 = strs[i].Text[j];
  
              //txt =(`Sections: ${t0} Text:${t1}`);
              //anchor.innerText = txt;
  
              var elem0 = document.createElement("li"); 
              var elem1 = document.createElement("li");
              elem0.innerText = t0
              anchor.innerText = t1
              
  
              //anchor.id = "articleSentence" + i;
              anchor.addEventListener("click", function()
              {
                  selectSentence(t0,t1);
              }); 
  
              elem1.appendChild(anchor);
  
              var elemtt = document.createElement("ul");
              elemtt.appendChild(elem0);
              elemtt.appendChild(elem1);
              innerItem.appendChild(elemtt);
              list.appendChild(innerItem);
          }
          
      }
  }
      $(function() 
      {
        $('a#calculate').bind('click', function() 
        {
          $.getJSON($SCRIPT_ROOT + '/ajaxGetArticle', 
          {
            valArticle: $('input[name="article"]').val()
          }, function(data) 
          {
            //$("#resultArticle").text(data.result);
            displayDocument(data.result);
          });
          
          return false;
        });
  
        $('a#calcAnalyzeRegex').bind('click', function() 
        {
          $.getJSON($SCRIPT_ROOT + '/ajaxAnalyzeRegex', 
          {
            valSentenceToAnalyze: $('textArea[name="analyzeRegex"]').val()
          }, function(data) 
          {
            $("#resultAnalyzeRegex").text(data.result);
          });
          return false;
        });
      });