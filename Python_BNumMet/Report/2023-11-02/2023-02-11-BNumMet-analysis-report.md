# Code analysis
## BNumMet 
#### Version 1 

**By: default**

*Date: 2023-02-11*

## Introduction
This document contains results of the code analysis of BNumMet



## Configuration

- Quality Profiles
    - Names: Sonar way [Python]; Sonar way [XML]; 
    - Files: AYZBMw64a-vbeyS_HRwm.json; AYZBMxa7a-vbeyS_HSdh.json; 


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



### Metrics

Coverage | Duplications | Comment density | Median number of lines of code per file | Adherence to coding standard |
:---:|:---:|:---:|:---:|:---:
96.8 % | 0.0 % | 36.7 % | 156.0 | 99.8 %

### Tests

Total | Success Rate | Skipped | Errors | Failures |
:---:|:---:|:---:|:---:|:---:
65 | 100.0 % | 0 | 0 | 0

### Detailed technical debt

Reliability|Security|Maintainability|Total
---|---|---|---
-|-|0d 5h 22min|0d 5h 22min


### Metrics Range

\ | Cyclomatic Complexity | Cognitive Complexity | Lines of code per file | Coverage | Comment density (%) | Duplication (%)
:---|:---:|:---:|:---:|:---:|:---:|:---:
Min | 0.0 | 0.0 | 0.0 | 93.5 | 19.2 | 0.0
Max | 207.0 | 202.0 | 1240.0 | 100.0 | 60.4 | 0.0

### Volume

Language|Number
---|---
Python|1240
Total|1240


## Issues

### Issues count by severity and types

Type / Severity|INFO|MINOR|MAJOR|CRITICAL|BLOCKER
---|---|---|---|---|---
BUG|0|0|0|0|0
VULNERABILITY|0|0|0|0|0
CODE_SMELL|0|95|2|3|0


### Issues List

Name|Description|Type|Severity|Number
---|---|---|---|---
Cognitive Complexity of functions should not be too high|Cognitive Complexity is a measure of how hard the control flow of a function is to understand. Functions with high Cognitive Complexity will be <br /> difficult to maintain. <br /> See <br />  <br />    Cognitive Complexity  <br /> |CODE_SMELL|CRITICAL|3
Function names should comply with a naming convention|Shared coding conventions allow teams to collaborate efficiently. This rule checks that all function names match a provided regular expression. <br /> Noncompliant Code Example <br /> With the default provided regular expression: ^[a-z_][a-z0-9_]*$ <br />  <br /> def MyFunction(a,b): <br />     ... <br />  <br /> Compliant Solution <br />  <br /> def my_function(a,b): <br />     ... <br /> |CODE_SMELL|MAJOR|2
Method names should comply with a naming convention|Sharing some naming conventions is a key point to make it possible for a team to efficiently collaborate. This rule allows to check that all method <br /> names match a provided regular expression. <br /> Noncompliant Code Example <br /> With default provided regular expression: ^[a-z_][a-z0-9_]*$ <br />  <br /> class MyClass: <br />     def MyMethod(a,b): <br />         ... <br />  <br /> Compliant Solution <br />  <br /> class MyClass: <br />     def my_method(a,b): <br />         ... <br /> |CODE_SMELL|MINOR|20
Field names should comply with a naming convention|Sharing some naming conventions is a key point to make it possible for a team to efficiently collaborate. This rule allows to check that field <br /> names match a provided regular expression. <br /> Noncompliant Code Example <br /> With the default regular expression ^[_a-z][_a-z0-9]*$: <br />  <br /> class MyClass: <br />   myField = 1 <br />  <br /> Compliant Solution <br />  <br /> class MyClass: <br />   my_field = 1 <br /> |CODE_SMELL|MINOR|34
Local variable and function parameter names should comply with a naming convention|Shared naming conventions allow teams to collaborate effectively. This rule raises an issue when a local variable or function parameter name does <br /> not match the provided regular expression. <br /> Exceptions <br /> Loop counters are ignored by this rule. <br />  <br /> for i in range(limit):  # Compliant <br />     print(i) <br /> |CODE_SMELL|MINOR|41


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

