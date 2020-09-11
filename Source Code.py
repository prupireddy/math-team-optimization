# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:11:36 2019

@author: Pranav Rupireddy1
"""

#Goal: Max out score on the inidivuals
#Constraint 1: 8 people -currently I cut off the matrix at top 8 scorers, but you could add in 0,0 at the perm stage (Check Line 36)
#Constraint 2: 4 people on each event - ConstraintTwoCheck Function
#Constrant 3: 2 events for each person - Set up assumes this

#General Program:
# 1. Creates all possibilities of two events assigned to each of the people
# 2. Filters 1) out to return all possibilities to where there are exactly 4 people on each event and
# then finds all possible ways to assign these to people
# 3. Plugs in these possibilities and creates a list of expected team scores from the possibilities
# 4. Sorts these possibilities in ascending order and congruently sorts their respective input 
# 5. Flips the sorted input and output matrices, stacks them, then renders this as an output 

#Throughout the program:   A=1 B=3 C=5 D=7. floor((number)/2) = real index in the ScoreMatrix. This 
#equation is super important. For the last column, look at the function Expansion.
#Job assignments take the form of a two digit numbers. For example, 13 = events A & B. I chose to 
#use this format because it made it easier to work with. 

from itertools import *
from math import *
from numpy import *
from sympy.utilities.iterables import multiset_permutations

'''
Use this as a guide for you to remember which person corresponds to which row in the Matrix below (each row in 
matrix refers to a person and each column = event - column 1 = A, 2 = B,3 = C, 4 = D, 5 = used for more than 8
people - look at the function Expansion)
Rupireddy
Subramanian
Priebe
King
Fairborne
S. Theis
Sadie
C. Theis
'''
   
# Divide your average score and divide that up among your top two predicted events. Fill up
#the remaining two events with the constraint that they (individually) should be , at the most, 
#the second highest score

SampleScoreMatrix = array([[3,2,3.5,4.5,0], 
                           [3.3,2.9,3.2,3.5,0], 
                           [2.5,1,2,1,0],
                           [.25,0,.75,.15,0], 
                           [1.5,2.2,1.5,2,0], 
                           [2.3,2.1,2,1,0], 
                           [1.67,.3,1,.2,0], 
                           [1.25,.25,.25,.75,0]] )
    
#This filters out all the job possibilities to only those where there are exactly four on each event. 
#It does this by finding the product of all the digits that are in the list of the digits - if there are exactly
#four on each event, then there the product should equal 1215560625: (1)^(4) * (3)^4 * (5)^4 * (7)^4 
#b/c each event will come up 4 times 
def SecondConstraint(OriginalMatrix):
    JobPossibilities = []
    for element in OriginalMatrix:
        RunningProduct = 1
        for subelement in element:
            RunningProduct = RunningProduct*floor(subelement/10)*(subelement%10)
        if RunningProduct == 121550625:
            JobPossibilities.append(element)
        else:
            1+1
    return JobPossibilities
 
#Expands out each of the viable (4 each event) possibility by finding all the permuations of the job possibility (every way to order them)
#Each order corresponds to the job being assigned to a particular person (thus why I call it an 
#assignment array at this point vs possibility array as in the previous steps) There is an additional feature at line 86 - this lets you
#maximize on more than 8 people. For each person over 8 - add on the element of 88. If you look at the Score Matrix above, 
#this gives you an expected score of floor(8/2) = 4 = column 5 = 0, which means that each person assigned to 88 effectively is not part of that
#team. Therefore, the number of people over 8 should be the number of people inactive as 8 is the max
#for the math team. So adding in the corresponding number of 88 lets you generate all the assignments
#when you have over 8 people. This will create a list of lists, where the latter refers to each job assignment set ([13,24 ...])

def Expansion(OriginalMatrix):
    AssignmentsArray = []
    for element in ActualJobs:
         #element.append(88,88)  - use how many 88's here as there is more total people than 8 people (10 people = 2 88)
         NewElement= list(multiset_permutations(element))
         AssignmentsArray.extend(NewElement)
    return AssignmentsArray

#This takes in each input (like each job assignment set - [13,24 ...]) and creates the expected team score with this lineup. 
#It does this by interating through each of the people within each of the assignment set (remember index of element of 
#job in assignment list = row = person) and plugging in the respective numbers from the matrix of expected scores
#,by breaking down the double digit numbers into single digits and converting them to the indices using floor(number/2).
#It adds these scores to a running total. When finished with an assignment set, the running total, the output,is appended to the output array.
#This, in effect, creates a list that stores all of the expected team scores with all lineups.
def GenerateOutputs(AssignmentsArray, DataMatrix, OutputArray):
    AssignmentIndex = 0
    for element in AssignmentsArray:
        i = 0
        RunningTotal = 0
        for subelement in element:
            RunningTotal = RunningTotal + DataMatrix[i][int(floor((floor(subelement/10))/2))] + DataMatrix[i][int(floor((subelement%10)/2))]
            i= i+1
        OutputArray[AssignmentIndex] = RunningTotal
        AssignmentIndex = AssignmentIndex + 1
    return OutputArray

#Takes in the sorted and unsorted lists of expected team outputs, and the list of the list of the original inputs.
#This sorts the list of inputs so that it corresponds with the sorted list of outputs. It does this my looping through
#each of the numbers in the sorted outputs, finding the number in the unsorted list of outputs, recording this index, 
#then putting the input with that index in the new sorted list 
def SortedInputs(InputArray,RegularOutput,SortedOutput):
    i = 0
    SortedInputArray = list(zeros(44730))
    for number in SortedOutput:
        index = RegularOutput.index(number)
        SortedInputArray[i] = InputArray[index]
        RegularOutput.remove(number)
        InputArray.remove(InputArray[index])
        i = i + 1
    return SortedInputArray

#Start of actual program    
#This creates all of the possible job possibilitiies, without assigning the job to any particular person.
#(i.e. Someone takes AC, another AD etc. without stating specifically WHO takes each)
TotalJobPossibilities = list(combinations_with_replacement([13,15,17,35,37,57], 8))

ActualJobs = []

#At this point, the second constraint has filtered out the job possibilities that will not have exactly 4 on each event
ActualJobs = SecondConstraint(TotalJobPossibilities)

#This "expands out" each of the job possibilities by generating all the ways to order the list of jobs. 
#Each ordered  arrangement corresponds to a way to distribute the jobs among people (i.e. if 13 comes up first
#the person who has first row in the matrix would get AC vs if 35 comes up first, the first person in the 
#row in would BC)
TotalJobAssignments = Expansion(ActualJobs)

#This now uses the job assignments as input and correspondingly creates the output for expected team sum,
#,storing it in AssignmentOutputs
AssignmentsOutputs = zeros(44730)
AssignmentsOutputs = list(GenerateOutputs(TotalJobAssignments,SampleScoreMatrix,AssignmentsOutputs))

#Sorts the outputs in ascending order and sorts the input so that they correspond with the outputs   
SortedOutputs = sorted(AssignmentsOutputs, reverse = True)
SortedInputs = SortedInputs(TotalJobAssignments,AssignmentsOutputs,SortedOutputs)

#Creates the final output by flipping the sorted (in ascending order) list of expected team score and 
#horizontally stacking with the corresponding assignments that would yield that team score 

SortedOutputsColumnVector = matrix(SortedOutputs).T
SortedInputsColumnVector = matrix(SortedInputs)
FinalOutput = hstack((SortedInputsColumnVector, SortedOutputsColumnVector))
set_printoptions(precision = 3)
savetxt("SubjectAssignmentOutput.txt", FinalOutput, fmt='%f')

#The final output will be stored in the same folder in which this python program is stored 