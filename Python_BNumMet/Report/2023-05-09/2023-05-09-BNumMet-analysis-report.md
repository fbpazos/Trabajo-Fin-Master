# Code analysis
## BNumMet 
#### Version 1 

**By: default**

*Date: 2023-05-09*

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
98.2 % | 0.0 % | 42.5 % | 210.0 | 99.8 %

### Tests

Total | Success Rate | Skipped | Errors | Failures |
:---:|:---:|:---:|:---:|:---:
96 | 100.0 % | 0 | 0 | 0

### Detailed technical debt

Reliability|Security|Maintainability|Total
---|---|---|---
-|-|0d 1h 30min|0d 1h 30min


### Metrics Range

\ | Cyclomatic Complexity | Cognitive Complexity | Lines of code per file | Coverage | Comment density (%) | Duplication (%)
:---|:---:|:---:|:---:|:---:|:---:|:---:
Min | 0.0 | 0.0 | 2.0 | 95.7 | 0.0 | 0.0
Max | 300.0 | 274.0 | 2111.0 | 100.0 | 61.5 | 0.0

### Volume

Language|Number
---|---
Python|2111
Total|2111


## Issues

### Issues count by severity and types

Type / Severity|INFO|MINOR|MAJOR|CRITICAL|BLOCKER
---|---|---|---|---|---
BUG|0|0|0|0|0
VULNERABILITY|0|0|0|0|0
CODE_SMELL|0|7|2|4|0


### Issues List

Name|Description|Type|Severity|Number
---|---|---|---|---
String literals should not be duplicated|Duplicated string literals make the process of refactoring error-prone, since you must be sure to update all occurrences. <br /> On the other hand, constants can be referenced from many places, but only need to be updated in a single place. <br /> Noncompliant Code Example <br /> With the default threshold of 3: <br />  <br /> def run(): <br />     prepare("this is a duplicate")  # Noncompliant - "this is a duplicate" is duplicated 3 times <br />     execute("this is a duplicate") <br />     release("this is a duplicate") <br />  <br /> Compliant Solution <br />  <br /> ACTION_1 = "action1" <br />  <br /> def run(): <br />     prepare(ACTION_1) <br />     execute(ACTION_1) <br />     release(ACTION_1) <br />  <br /> Exceptions <br /> No issue will be raised on: <br />  <br />    duplicated string in decorators  <br />    strings with less than 5 characters  <br />    strings with only letters, numbers and underscores  <br />  <br />  <br /> @app.route("/api/users/", methods=['GET', 'POST', 'PUT']) <br /> def users(): <br />     pass <br />  <br /> @app.route("/api/projects/", methods=['GET', 'POST', 'PUT'])  # Compliant <br /> def projects(): <br />     pass <br /> |CODE_SMELL|CRITICAL|1
Cognitive Complexity of functions should not be too high|Cognitive Complexity is a measure of how hard the control flow of a function is to understand. Functions with high Cognitive Complexity will be <br /> difficult to maintain. <br /> See <br />  <br />    Cognitive Complexity  <br /> |CODE_SMELL|CRITICAL|3
Function names should comply with a naming convention|Shared coding conventions allow teams to collaborate efficiently. This rule checks that all function names match a provided regular expression. <br /> Noncompliant Code Example <br /> With the default provided regular expression: ^[a-z_][a-z0-9_]*$ <br />  <br /> def MyFunction(a,b): <br />     ... <br />  <br /> Compliant Solution <br />  <br /> def my_function(a,b): <br />     ... <br /> |CODE_SMELL|MAJOR|2
Local variable and function parameter names should comply with a naming convention|Shared naming conventions allow teams to collaborate effectively. This rule raises an issue when a local variable or function parameter name does <br /> not match the provided regular expression. <br /> Exceptions <br /> Loop counters are ignored by this rule. <br />  <br /> for i in range(limit):  # Compliant <br />     print(i) <br /> |CODE_SMELL|MINOR|7


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
