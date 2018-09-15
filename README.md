# GENIVI-GSoC-18

GENIVI GSoC 2018 is the official repository for the project VCIVING Voice Control for IVI Next Generation project kickstarted by Google Summer of Code 2018. Visit the [Wiki](https://at.projects.genivi.org/wiki/display/PROJ/%5BGSOC+2018%5D+VCIVING+Voice+Control+for+IVI+Next+Generation) for more information.
Visit the [Overview of VCIVING](https://at.projects.genivi.org/wiki/display/PROJ/Overview+of+VCIVING) page to gain a basic understanding of the project.

## Introduction to VCIVING

VCIVING is a voice controlling system for IVI. It's more or less an assistant to interact with IVI using voice. VCIVING functions as an individual entity from the IVI systems and interacts with IVI whenver necessary.

## Contents

- Brain: Interfaces and classes required for basic functionality such as grabbing inputs, providing outputs, and also the classes required to train the models.
- EmulationCore: Entry points to the system. Contains mainly the event handlers and directives to various sections of the system and performs functions such as speech recognition and interpretation.
- TaskExecutors: Interfaces which addresses functions related to the IVI system such as playing music.
- Trainer: The scripts for training various models such as Speech Interpretation.

## Installation
Build instructions and project pages are found here:
https://at.projects.genivi.org/wiki/display/PROJ/%5BGSOC+2018%5D+VCIVING+Voice+Control+for+IVI+Next+Generation

## Special Note

We've incorporated [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) on to EmulationCore instead of Google Speech Recognition APIs. Please consult [this page](https://github.com/GENIVI/GENIVI-GSoC-18/blob/migration/DeepSpeech/EmulationCore/Readme.MD) during the installation.
More details will be added later.
