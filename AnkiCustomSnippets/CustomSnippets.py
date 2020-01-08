from aqt import editor
from anki.hooks import addHook
from aqt.utils import showInfo
import inspect
import os
import re

global posIdx
global caretPositions

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

// Move caret to end of word
var s = window.getSelection();
var r = s.getRangeAt(0);
var fieldContent = currentField.innerHTML;
r = s.getRangeAt(0);
r.setStart(r.startContainer, r.startOffset + currentField.innerHTML.length);
r.collapse(true);
s.removeAllRanges();
s.addRange(r);
"""

# Modified from function wrap() in Anki's editor.js
moveCaretToPos = """
var shift = %s;

var s = window.getSelection();
var r = s.getRangeAt(0);

r = s.getRangeAt(0);
r.setStart(r.startContainer, r.startOffset + shift);
r.collapse(true);
s.removeAllRanges();
s.addRange(r);
"""

def onSetupShortcuts(cuts, self):
    cuts.append(("Shift+Tab", self.insertSnippet))
    cuts.append(("Ctrl+J", self.nextCaretPos))

def insertSnippet(self):
    global caretPositions
    global posIdx
    posIdx = 0
    matched = list(re.finditer(r'\$\d', snippet))
    indices = [matched[i].start() for i in range(len(matched))]
    indicesCorrected = [indices[i] - 2*i for i in range(len(indices))]  # Correct for additional two characters with $\d
    positions = [int(matched[i].group()[1]) for i in range(len(matched))]

    caretPositions = list(zip(indicesCorrected, positions))
    caretPositions.sort(key = lambda t: t[1])
    toInsert = re.sub(r'\$\d', '', snippet)
    # self.web.eval('currentField.innerHTML = "' + toInsert + '";')
    self.web.eval(insertInput % toInsert)
    self.web.eval(moveCaretToPos % (caretPositions[0][0] - len(toInsert)))
    posIdx += 1

def nextCaretPos(self):
    try:
        global caretPositions
        global posIdx
        self.web.eval(moveCaretToPos % (caretPositions[posIdx][0] - caretPositions[posIdx-1][0]))
        posIdx += 1
    except:
        pass

editor.Editor.insertSnippet = insertSnippet
editor.Editor.nextCaretPos = nextCaretPos
addHook("setupEditorShortcuts", onSetupShortcuts)
