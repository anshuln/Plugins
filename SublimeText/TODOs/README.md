# TODO Helper
A plugin to track specific comments in your project. All comments comments with the required phrase are collated into a separate file.

## How to use
* Copy the entire directory into your `sublime-text-3/Packages` directory
* Edit the `TODO_config.json` file according to your language and project preferences. The plugin collects all comments containing `pattern` (case insensitive), leaving out all comments with `done_pattern`, and writes them into `write_file`. `fn_identifier` is for figuring out which function contained the comment, and only lines with `comment_identifier` are examined. An example config file for Python is shown
* Run `TODO` in the command palette to run the package on the current file.
