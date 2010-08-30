// ==UserScript==
// @name           Annotator
// @namespace      annotator
// @include        http://*
// @author          Allagappan  (alagu@alagu.net)
// ==/UserScript==
//
//

// Get ID

(function(){
function $(ID) {return document.getElementById(ID);}
//var isInIFrame = (window.location != window.parent.location) ? true : false;
var isInIFrame = false;



if(!isInIFrame) 
{

    var getXpath = function(node) {

        var e = node;
        
        for (var path = ''; e && e.nodeType == 1; e = e.parentNode) {
            var predicate = [];
            var brothers = e.parentNode.children;
            var count = 0;
            var unique = false;
            for (var i = 0; brothers && (i < brothers.length); i++) {
                if (brothers[i].tagName == e.tagName) {
                    count++;
                    if (brothers[i] == e) {
                        idx = count;
                    }
                }
            }
            if (idx == 1 && count == 1) {
                idx = null;
            }
          if (e.id) {
            predicate[predicate.length] = "@id='" + e.id + "'";
            unique = true;
          }
          if (e.className) {
            predicate[predicate.length] = "@class='" + e.className + "'";
          }
          //idx = ( useIdx && idx && !unique ) ? ('[' + idx + ']') : '';
          predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : '';
          path='/' + e.tagName.toLowerCase() +  predicate + path;
          //path = '/' + path;
        }

        return path;
    }

    var tgt = null;
    var focusobj = function(target){
        if(tgt) {
        tgt.style.border="";
        tgt.style.borderColor="";
        tgt.style.borderStyle="";
        }

        tgt = target;
        var xpath = getXpath(tgt);
        document.getElementById('xpath').value = xpath;

        tgt.style.border="2px";
        tgt.style.borderColor="#f00";
        tgt.style.borderStyle="solid";

    }


    var nextXpath = function() {
        if(!resultObj) return;
        console.log(resultObj);
        if(resultObj.resultSet.length == resultObj.curItem + 1) {
            document.getElementById('xpath-test-value').innerHTML  = 'End of Items';
            return;
        }

        resultObj.curItem++; 
        var curNode = resultObj.resultSet[resultObj.curItem];
        focusobj(curNode);
        curNode.scrollIntoView();
        document.getElementById('xpath-test-value').innerHTML = curNode.textContent;
    }


    var addXpath = function() {
        var xpathNode = document.getElementById('xpath');
        var xpathKey = document.getElementById('xpath-key');

        if(xpathKey.value.length < 1) {
            alert('Give a name for xpath');
        }
        else
        {
            localStorage.setItem(xpathKey.value, xpathNode.value);
            console.log(localStorage);
            var k = localStorage.getItem('keys');
            if(k== null) 
           {
                localStorage.setItem('keys', xpathKey.value);
            }
            else
            {
                localStorage.setItem('keys', k + ','  + xpathKey.value);
            }
        }
    }

    var resultObj = {};
    resultObj.resultSet = {};
    resultObj.curItem = 0;



    var showXpaths = function() {
        var table = document.getElementById('xpath-table');
        var but   = document.getElementById('show-xpath');


        if(table.style.display != 'none') {
            table.style.display = 'none';
            but.value = 'Show Xpaths';
        }
        else {
            but.value = 'Hide Xpaths';
            table.style.display = 'block';
            var prevKeys = localStorage.getItem('keys').split(',');
            if(prevKeys.length != 0) 
            {
                for(var i=0;i<prevKeys.length;i++)
                {
                    var trNode = document.createElement('tr');
                    console.log(prevKeys[i]);
                    var tdKey = document.createElement('td');
                    var tdValue = document.createElement('td');
                    tdKey.innerHTML = prevKeys[i];
                    tdValue.innerHTML = localStorage.getItem('title');
                    tdValue.style.overflow = "hidden";
                    tdValue.style.height   = "30px";
                    tdValue.style.width   = "30px";

                    trNode.appendChild(tdKey);
                    trNode.appendChild(tdValue);
                    table.appendChild(trNode);
                }
            }
        }
    }

    var testXpath = function() {
        document.getElementById('next-xpath').style.display = 'none';
        var xpathNode = document.getElementById('xpath');
        var xpathResults = document.getElementById('xpath-test-value');
        var xpath = xpathNode.value;

        if(xpath.length == 0)
        {
           xpathResults.innerHTML = 'No xpath available'; 
        } else {
           xpathResults.innerHTML = 'Evaluating..'; 
           var results = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null ); 

           var resultItem = results.iterateNext();
           resultObj.resultSet = [resultItem];
           resultObj.curItem   = 0;

           while (resultItem) {
               resultItem = results.iterateNext();
               if(resultItem) {
                   resultObj.resultSet[resultObj.resultSet.length] = resultItem;
               }
           }

           if(resultObj.resultSet.length == 1){
               xpathResults.innerHTML = resultObj.resultSet[0].textContent; 
           }
           else
           {
               xpathResults.innerHTML = resultObj.resultSet[0].textContent;
               document.getElementById('next-xpath').style.display = '';
           }

        }
    }

    document.body.addEventListener('click',function(evt){
            if(evt.target.id != 'xpath-key' &&
               evt.target.id != 'xpath' &&
               evt.target.id != 'add-xpath' && 
               evt.target.id != 'test-xpath' &&
               evt.target.id != 'show-xpath' &&
               evt.target.id != 'next-xpath' &&
               evt.target.id != 'xpath-test-value') {
                focusobj(evt.target);
            }

            if(evt.target.id == 'test-xpath') {
                testXpath();
            }

            if(evt.target.id == 'add-xpath') {
                addXpath();
            }

            if(evt.target.id == 'next-xpath') {
                nextXpath();
            }

            if(evt.target.id == 'show-xpath') {
                showXpaths();
            }

            return false;
     },
    false);


    var dv = document.createElement('div');
    dv.innerHTML = ['<div><input type="text" name="xpath" id="xpath">','<input type="text" id="xpath-key" name="key">',
                    '<input type="submit" id="add-xpath" value="Add Xpath">',
                    '<input type="button" id="test-xpath" value="Test Xpath"></div>',
                    '<div><span id="xpath-test-value"> &nbsp; </span>',
                    '<input type="button" id="next-xpath" value="Next result">',
                    '<input id="show-xpath" type="button" value="Show Xpaths"></div>',
                    '<div id="xpath-list"><table border=1 width="100%" style="color:#000" id="xpath-table">',
                    '<tr><th width="50%">Name</th><th width="50%">XPath</th></tr>',
                    '</table></div>'].join(' ');
    dv.style.backgroundColor="orange";
    dv.style.position="fixed";
    dv.style.bottom="0";
    dv.style.right="0";
    dv.style.padding="5px";
    document.body.appendChild(dv);
    var xpathtest = document.getElementById('xpath-test-value');
    xpathtest.style.width="236px";
    xpathtest.style.height="22px";
    xpathtest.style.display="inline-block";
    xpathtest.style.overflow="hidden";
    xpathtest.style.color='#f00';
    xpathtest.style.fontSize = "13px";
    xpathtest.style.padding="5px";
    xpathtest.innerHTML = 'Your results will come here';
    document.getElementById('next-xpath').style.display = 'none';
    document.getElementById('xpath-table').style.display = 'none';
}

})();
