from aqt import editor
from anki.hooks import addHook
from aqt.utils import showInfo
import inspect
import os
import re

global toInsert
global posIdx
# global caretPositions

# To fix:
# - Moving cursor once input is added
# - Using this several times

prompt = "frac"

# Need four backslashes to escape backslash when it is in Python, and again when passed to JavaScript
snippet = "\\\\frac{$2}{$1}$3"

insertInput = """
var input = "%s";
var theirInput = currentField.innerHTML;
currentField.innerHTML = theirInput.concat(input);
var idx = currentField.innerHTML.indexOf("$1");
currentField.innerHTML = currentField.innerHTML.replace("$1", "");

var s = window.getSelection();
var r = s.getRangeAt(0);
r = s.getRangeAt(0);
r.setStart(r.startContainer, r.startOffset + idx);
r.collapse(true);
s.removeAllRanges();
s.addRange(r);

var prevIdx = idx;
"""

# Modified from function wrap() in Anki's editor.js
replace = """
var pos = %s;

var theirInput = currentField.innerHTML;
var idx = theirInput.indexOf("$".concat(pos));

//var newInput = currentField.innerHTML.replace("$".concat(pos), "");
//currentField.innerHTML = newInput;

s = window.getSelection();
r = s.getRangeAt(0);
r.setStart(r.startContainer, r.startOffset + idx - prevIdx + 2);
r.collapse(true);
s.removeAllRanges();
s.addRange(r);
"""

def getFieldContents():
    test = self.web.evalWithCallback

def onSetupShortcuts(cuts, self):
    cuts.append(("Shift+Tab", self.insertSnippet))
    cuts.append(("Ctrl+J", self.nextCaretPos))

def insertSnippet(self):
    # global caretPositions
    global posIdx
    global toInsert
    posIdx = 1
    # matched = list(re.finditer(r'\$\d', snippet))
    # indices = [matched[i].start() for i in range(len(matched))]
    # indicesCorrected = [indices[i] - 2*i for i in range(len(indices))]  # Correct for additional two characters with $\d
    # positions = [int(matched[i].group()[1]) for i in range(len(matched))]
    #
    # caretPositions = list(zip(indicesCorrected, positions))
    # caretPositions.sort(key = lambda t: t[1])
    # toInsert = re.sub(r'\$\d', '', snippet)
    # # self.web.eval('currentField.innerHTML = "' + toInsert + '";')
    toInsert = snippet
    # position = toInsert.find("$1")
    # toInsert = toInsert.replace("$1", "")
    self.web.eval(insertInput % toInsert)
    # self.web.eval(moveCaret % (position - len(toInsert)))
    posIdx += 1

def nextCaretPos(self):
    global toInsert
    try:
        # global caretPositions
        global posIdx
        self.web.eval(replace % 2)
        posIdx += 1
    except:
        pass

editor.Editor.insertSnippet = insertSnippet
editor.Editor.nextCaretPos = nextCaretPos
addHook("setupEditorShortcuts", onSetupShortcuts)
