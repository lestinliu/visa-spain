# Created by automation at 4/29/19
Feature: #Enter feature name here
  # Enter feature description here

  Scenario: # Enter scenario name here
    Given open page
    When select centre "Minsk"
    And select category "Normal"
    And enter phone number "256062209"
    And enter email "sash.kardash@gmail.com"
    And enter random code
    And click "request code" button
    And enter code from email
    And click "continue" button
    And click "accept" button

    And select all available dates and times

    And select travel date "22/11/2019"
    And select visa type "Tourism"
    And enter first name "Alexandr"
    And enter last name "Kardash"
    And select birthday "22/11/2019"
    And enter pasport number "AB123456"
    And select issued date "22/11/2019"
    And select expired date "22/11/2019"
    And enter issued city "Ивацевичи"
    And enter captcha
    And click "submit" button