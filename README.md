# Point-and-Select Operation based on Voice Control

This repository contains the codebase developed as part of my master's thesis, titled **"Point-and-Select Operation based on Voice Control"**, submitted to the University of Rijeka, Faculty of Engineering, in September 2023. The codebase is developed for the **Windows** operating system.

## About the Thesis

This project explores alternative methods of cursor control using voice commands, offering six distinct interaction modalities. Each modality combines different approaches to cursor movement (continuous or discrete) and direction determination (e.g., angular input or pre-set directions). It was implemented and tested as a proof-of-concept to evaluate usability, intuitiveness, and performance.

The study involved experiments with 16 participants, employing metrics like Fitts' law to measure task completion time and user experience.

For detailed information, refer to the full thesis: [URN: https://urn.nsk.hr/urn:nbn:hr:190:025397](https://urn.nsk.hr/urn:nbn:hr:190:025397)

---

## Features

- **Six Voice-Controlled Modalities**:
  1. Continuous movement with directional commands (e.g., *up, down*).
  2. Discrete movement specifying pixel distances with directional commands (e.g., *up 100*).
  3. Continuous movement with direction determined by angular values.
  4. Discrete movement with direction determined by angular values.
  5. Continuous movement with animated cursor direction indication.
  6. Discrete movement with animated cursor direction indication.
  
- **Experimental Applications**:
  - A custom Python-based testing application to measure performance and collect results.

---

## Technologies Used

- **Programming Language**: Python
- **Libraries**:
  - `SpeechRecognition` for voice input processing.
  - `Vosk` for offline speech recognition.
  - `multiprocessing` for concurrent task handling.
  - `mouse` and `keyboard` for input control simulation.
  - `tkinter` for GUI development.
  - `ctypes` for cursor customization.
- **Development Tools**:
  - **Axialis CursorWorkshop** for custom animated cursors.

---

## Installation

1. Clone the repository:
2. Create a virtual environment in Python:

      ```
      python -m venv <env_name>
      ```
3. Activate the virtual environment:
      ```
      <env_name>\Scripts\activate
      ```
4. Install necessary packages from ``requirements.txt`` located at the root of this repository.
      ```
      pip freeze > requirements.txt
      ```

## Usage 

1. **Run a Modal Interaction:** Each modality has a separate script that can be executed to control the pointer using voice commands. For example:

      ```
      python mode1.py
      ```

2. **Test Modalities:** Use the provided testing application to evaluate performance:

      ```
      python mode_testing_app.py
      ```
3. **Stop the Program:**

    Press `q` to exit any modality.

## Testing
-  The `mode_testing_app.py` script guides users through a predefined task to evaluate each modality's performance.
-  Results are stored in a CSV file, capturing completion time and other metrics.