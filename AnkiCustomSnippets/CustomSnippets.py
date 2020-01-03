from aqt import editor
from anki.hooks import addHook
from aqt.utils import showInfo
import inspect
import os

replaceJS = """
var snippets = [['mrm', 'mathrm'], ['mbf', 'mathbf'], ['l', 'lol']];
theirInput = currentField.innerHTML;

for (var i = 0; i < snippets.length; i++) {
    if (theirInput.endsWith(snippets[i][0])) {
        var toReplace = currentField.innerHTML.replace(snippets[i][0], snippets[i][1]);
        currentField.innerHTML = toReplace;
    }
}
"""

# replaceJS = """document.write(currentField.innerHTML);"""

def onSetupShortcuts(cuts, self):
    cuts.append(("Shift+Tab", self.insertArbitraryWrapper))

def insertArbitraryWrapper(self):
    # self.web.eval(replaceJS)
    self.web.eval(replaceJS)
    # showInfo(self.web.eval("currentField.innerHTML"))
    # output = self.web.evalWithCallback("currentField.innerHTML;", lambda x : x)
    # logFile.write(str(inspect.getmembers(self.currentField)))
    # showInfo(str(type(inspect.getmembers(self.currentField))))
    # showInfo(str(self.currentfield))
    # self.web.eval("document.write('test output')")

logFile = open(os.path.expanduser("~/Desktop/LogOut.txt"), "w+")

editor.Editor.insertArbitraryWrapper = insertArbitraryWrapper
addHook("setupEditorShortcuts", onSetupShortcuts)
