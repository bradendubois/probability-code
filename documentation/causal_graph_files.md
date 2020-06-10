# Causal Graph Files

This document outlines  the structure of how to create a causal graph file.

- The graph file must be a valid ``JSON`` file.
- By default, there is a folder labelled ``causal_graphs``, and any file in this directory with a ``.json`` file
    extension will by listed when starting the software.
    - The graph file can be placed anywhere and accessed through modifying the main file, ``ProPyBilityRunner.py`` where it checks/loads.

## Graph File Structure

The graph file must be structured as follows:

```json
{
  "name": "NAME_OF_VARIABLE",
  "variables": [{
    "name": "VARIABLE_NAME",
    "outcomes": ["OUTCOME_1,", "OUTCOME_2", "..."],
    "parents": ["PARENT_1", "PARENT_2", "..."],
    "determination": {
      "type": "table/function",
      "tables": [{
        "given": ["PARENT_1", "PARENT_2", "..."],
        "rows": [
          ["OUTCOME_1", ["PARENT_1_OUTCOME_1", "PARENT_2_OUTCOME_1", "..."], 0.0],
          ["OUTCOME_1", ["PARENT_1_OUTCOME_1", "PARENT_2_OUTCOME_2", "..."], 0.0],
          ["OUTCOME_1", ["PARENT_1_OUTCOME_2", "PARENT_2_OUTCOME_1", "..."], 0.0],
          ["..."]
        ]
      }]
    }
  }]
}
```

In detail:

- **"name"**: an optional parameter, allowing you to name the file; it will be displayed when the software is started,
as a helpful reminder of which files you're looking at.
- **"variables""**: A list of all the variables and their relevant tables/functions. Each variable must have the following:
    - **"name"**: The actual label of the variable itself, "X", "WEATHER", etc. Generally, it may be helpful to make this name uppercase. Must be unique.
    - **"outcomes"**: A list of strings, representing all possible outcomes for the given variable. Cannot have the same outcome twice in one variable, but two separate variables could have the same outcome.
    - **"parents"**: A list of strings, representing the "parents" of the given variable. Leave empty to represent zero parents.
    - **"determination"**: How the given variable is calculated/evaluated. Consists of the following:
        - **"type"**: Whether the given variable is determined by a table, or a function. Must have the value "table" or "function", respectively.
        - If the "type" is "table", the following attribute is necessary:
            - **"tables"**: A list of tables determining the given variable, each table consisting of the following:
                - **"given"**: A list of "given" variables, such as the parents of the variable.
                - **"rows"**: A list of lists, each list representing one "row" in the table, with each sublist formatted as follows:
                    - ["outcome", ["parent_1_outcome_1", "parent_2_outcome_1"], probability]
                    - "outcome" is a specific outcome of the given variable.
                    - The inner list is a specific combination of given outcomes, and they must be given in the same order as specified in "given", and a probability as a float.
                    - The table must be complete.
        - If the "type" is "function", ... ***THIS IS STILL BEING WRITTEN***
