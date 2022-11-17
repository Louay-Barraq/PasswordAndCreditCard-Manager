<h1 align='center'>Password Manager With Graphical User Interface</h1>

---

<p align="center">
  This password manager can store multiple services [accounts or credit cards] for multiple users.
  The users, their credit cards and their accounts are stored in a database.  
  All the passwords and credit card numbers get encrypted before getting stored in the database and get decrypted before being shown to the user when asked to. 
</p>


---


# Table of Contents
<ul>
	<li><a href="#-getting-started">Getting Started</a></li>
	<li><a href="#-features">Features</a></li>
	<li><a href="#to-do">To do</a></li>
</ul>

---

# 🚀 Getting Started
<h2> Prerequisites </h2>

<h3>To Clone The Project :</h3>
<ul>
	<li>Clone this repo using in the terminal:
</ul>

```
git clone git@github.com:Louay-Barraq/Password-Manager.git
```
<h3>To Install Python, You Can Simply :</h3>
<ul>
	<li>Windows
		<p>From <a href="http://python.org/download">python.org</a>, download the installer and install it. </p>
	</li>
	<li>Linux
		<p>Type on terminal:</p>
	</li>
</ul>

```
sudo apt-get install python3
```

<h3>Install required packages</h3>
<p>Open the terminal and run</p>

```
pip install cryptography PyQt5
```


<h2>Using</h2>
<p>To use the manager just open the terminal and run main.py with</p>

```
python3 main.py
```
<p>In case you want to execute the GUI version run the file gui_main.py</p>

```
python3 gui_main.py
```

---

# 📋 Features

- [X] Handling multiple users 
- [X] Adding or removing a user
- [X] Each user has his own key that helps in his passwords' encryption
- [X] Adding, removing and checking infos of any account the user has
- [X] Adding, removing and checking infos of any credit card the user has
- [X] Updating any of the account's infos
- [X] Updating any of the credit card's infos
- [X] Showing all the saved accounts
- [X] Showing all the saved credit cards
- [X] A Graphical User Interface [GUI] to make the user experience easier


<h2> Built with</h2>
<ul>
	<li>Core :
    		<p>
			<a href="python.org">Python</a> - A high-level interpreted programming language
		</p>
  	</li>
  	<li>Storage :
    	<p>
				<a href="https://www.sqlite.org">SQLite</a> -  
				a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
			</p>
  	</li>
		<li>GUI :
			<p>
			<a href='https://www.riverbankcomputing.com/software/pyqt/'>PyQt5</a> - 
				Bidings for <a href='https://www.qt.io/'>the QtCompany's</a> Qt application framework implemented as python modules
			</p>
      <p>
      <a href='https://build-system.fman.io/qt-designer-download'>Qt Designer</a> - A program that makes the process of making graphical user interfaces       easier
      </p>
      
			
</ul>
	
--- 

# 📝 License </h1>

<img alt="License" src="https://img.shields.io/badge/license-MIT-%2304D361">

This project is licensed under the MIT license - see the <a href="https://github.com/luis705/password-manager/blob/master/LICENSE">LICENSE</a> file for details
