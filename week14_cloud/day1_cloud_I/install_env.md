## Python env:

### 1. In the same path you have the project. Use next commands: 
1. pip3 install virtualenv
2. virtualenv -p python3 env
3. (\path\to\env)\Scripts\activate.bat

*Notice how your prompt is now prefixed with the name of your environment (env, in our case). This is the indicator that env is currently active, which means the python executable will only use this environment’s packages and settings*

4. With the (env) activated, you have to install every single library you use in your project :) with this:
    - pip3 install LIBRARY-NAME
    With "pip3 install --no-cache-dir LIBRARY-NAME" you install trying to avoid memory problems
5. After that use (in the root path of your project):
    - pip3 freeze > requirements.txt

**NOTE:** If there is an issue with 2 or 3 then try this: 
- sudo apt install python3-venv 

