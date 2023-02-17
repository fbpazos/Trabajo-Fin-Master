# Code analysis
## BNumMet 
#### Version 1 

**By: default**

*Date: 2023-02-17*

## Introduction
This document contains results of the code analysis of BNumMet



## Configuration

- Quality Profiles
    - Names: Sonar way [Python]; Sonar way [XML]; 
    - Files: AYZE7i3U2dITZFwgEli2.json; AYZE7jaV2dITZFwgEmPx.json; 


 - Quality Gate
    - Name: Sonar way
    - File: Sonar way.xml

## Synthesis

### Analysis Status

Reliability | Security | Security Review | Maintainability |
:---:|:---:|:---:|:---:
A | A | A | A |

### Quality gate status

| Quality Gate Status | OK |
|-|-|

Metric|Value
---|---
Reliability Rating on New Code|OK
Security Rating on New Code|OK
Maintainability Rating on New Code|OK
Coverage on New Code|OK
Duplicated Lines (%) on New Code|OK


### Metrics

Coverage | Duplications | Comment density | Median number of lines of code per file | Adherence to coding standard |
:---:|:---:|:---:|:---:|:---:
97.5 % | 0.0 % | 44.0 % | 209.0 | 99.7 %

### Tests

Total | Success Rate | Skipped | Errors | Failures |
:---:|:---:|:---:|:---:|:---:
77 | 100.0 % | 0 | 0 | 0

### Detailed technical debt

Reliability|Security|Maintainability|Total
---|---|---|---
-|-|0d 4h 16min|0d 4h 16min


### Metrics Range

\ | Cyclomatic Complexity | Cognitive Complexity | Lines of code per file | Coverage | Comment density (%) | Duplication (%)
:---|:---:|:---:|:---:|:---:|:---:|:---:
Min | 0.0 | 0.0 | 0.0 | 95.3 | 22.2 | 0.0
Max | 238.0 | 233.0 | 1652.0 | 100.0 | 74.1 | 0.0

### Volume

Language|Number
---|---
Python|1652
Total|1652


## Issues

### Issues count by severity and types

Type / Severity|INFO|MINOR|MAJOR|CRITICAL|BLOCKER
---|---|---|---|---|---
BUG|0|0|0|0|0
VULNERABILITY|0|0|0|0|0
CODE_SMELL|0|94|3|4|0


### Issues List

Name|Description|Type|Severity|Number
---|---|---|---|---
String literals should not be duplicated|Duplicated string literals make the process of refactoring error-prone, since you must be sure to update all occurrences. <br /> On the other hand, constants can be referenced from many places, but only need to be updated in a single place. <br /> Noncompliant Code Example <br /> With the default threshold of 3: <br />  <br /> def run(): <br />     prepare("this is a duplicate")  # Noncompliant - "this is a duplicate" is duplicated 3 times <br />     execute("this is a duplicate") <br />     release("this is a duplicate") <br />  <br /> Compliant Solution <br />  <br /> ACTION_1 = "action1" <br />  <br /> def run(): <br />     prepare(ACTION_1) <br />     execute(ACTION_1) <br />     release(ACTION_1) <br />  <br /> Exceptions <br /> No issue will be raised on: <br />  <br />    duplicated string in decorators  <br />    strings with less than 5 characters  <br />    strings with only letters, numbers and underscores  <br />  <br />  <br /> @app.route("/api/users/", methods=['GET', 'POST', 'PUT']) <br /> def users(): <br />     pass <br />  <br /> @app.route("/api/projects/", methods=['GET', 'POST', 'PUT'])  # Compliant <br /> def projects(): <br />     pass <br /> |CODE_SMELL|CRITICAL|1
Cognitive Complexity of functions should not be too high|Cognitive Complexity is a measure of how hard the control flow of a function is to understand. Functions with high Cognitive Complexity will be <br /> difficult to maintain. <br /> See <br />  <br />    Cognitive Complexity  <br /> |CODE_SMELL|CRITICAL|3
Function names should comply with a naming convention|Shared coding conventions allow teams to collaborate efficiently. This rule checks that all function names match a provided regular expression. <br /> Noncompliant Code Example <br /> With the default provided regular expression: ^[a-z_][a-z0-9_]*$ <br />  <br /> def MyFunction(a,b): <br />     ... <br />  <br /> Compliant Solution <br />  <br /> def my_function(a,b): <br />     ... <br /> |CODE_SMELL|MAJOR|2
Two branches in a conditional structure should not have exactly the same implementation|Having two branches in the same if structure with the same implementation is at best duplicate code, and at worst a coding error. If <br /> the same logic is truly needed for both instances, then they should be combined. <br /> Noncompliant Code Example <br />  <br /> if 0 &lt;= a &lt; 10: <br />     do_first() <br />     do_second() <br /> elif 10 &lt;= a &lt; 20: <br />     do_the_other_thing() <br /> elif 20 &lt;= a &lt; 50: <br />     do_first()         # Noncompliant; duplicates first condition <br />     do_second() <br />  <br /> Exceptions <br /> Blocks in an if chain that contain a single line of code are ignored. <br />  <br /> if 0 &lt;= a &lt; 10: <br />     do_first() <br /> elif 10 &lt;= a &lt; 20: <br />     do_the_other_thing() <br /> elif 20 &lt;= a &lt; 50: <br />     do_first()         # no issue, usually this is done on purpose to increase the readability <br />  <br /> But this exception does not apply to if chains without else-s when all branches have the same single line of code. In <br /> case of if chains with else-s rule S3923 raises a bug. <br />  <br /> if 0 &lt;= a &lt; 10: <br />     do_first() <br /> elif 20 &lt;= a &lt; 50: <br />     do_first()         # Noncompliant, this might have been done on purpose but probably not <br /> |CODE_SMELL|MAJOR|1
Method names should comply with a naming convention|Sharing some naming conventions is a key point to make it possible for a team to efficiently collaborate. This rule allows to check that all method <br /> names match a provided regular expression. <br /> Noncompliant Code Example <br /> With default provided regular expression: ^[a-z_][a-z0-9_]*$ <br />  <br /> class MyClass: <br />     def MyMethod(a,b): <br />         ... <br />  <br /> Compliant Solution <br />  <br /> class MyClass: <br />     def my_method(a,b): <br />         ... <br /> |CODE_SMELL|MINOR|20
Field names should comply with a naming convention|Sharing some naming conventions is a key point to make it possible for a team to efficiently collaborate. This rule allows to check that field <br /> names match a provided regular expression. <br /> Noncompliant Code Example <br /> With the default regular expression ^[_a-z][_a-z0-9]*$: <br />  <br /> class MyClass: <br />   myField = 1 <br />  <br /> Compliant Solution <br />  <br /> class MyClass: <br />   my_field = 1 <br /> |CODE_SMELL|MINOR|36
Local variable and function parameter names should comply with a naming convention|Shared naming conventions allow teams to collaborate effectively. This rule raises an issue when a local variable or function parameter name does <br /> not match the provided regular expression. <br /> Exceptions <br /> Loop counters are ignored by this rule. <br />  <br /> for i in range(limit):  # Compliant <br />     print(i) <br /> |CODE_SMELL|MINOR|38


## Security Hotspots

### Security hotspots count by category and priority

Category / Priority|LOW|MEDIUM|HIGH
---|---|---|---
LDAP Injection|0|0|0
Object Injection|0|0|0
Server-Side Request Forgery (SSRF)|0|0|0
XML External Entity (XXE)|0|0|0
Insecure Configuration|0|0|0
XPath Injection|0|0|0
Authentication|0|0|0
Weak Cryptography|0|0|0
Denial of Service (DoS)|0|0|0
Log Injection|0|0|0
Cross-Site Request Forgery (CSRF)|0|0|0
Open Redirect|0|0|0
Permission|0|0|0
SQL Injection|0|0|0
Encryption of Sensitive Data|0|0|0
Traceability|0|0|0
Buffer Overflow|0|0|0
File Manipulation|0|0|0
Code Injection (RCE)|0|0|0
Cross-Site Scripting (XSS)|0|0|0
Command Injection|0|0|0
Path Traversal Injection|0|0|0
HTTP Response Splitting|0|0|0
Others|0|0|0


### Security hotspots

