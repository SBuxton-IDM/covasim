import covasim as cv
import numpy as np
import unittest
from unittest_support_classes import CovaSimTest, TestProperties


# Suite of tests to test basic functionality of the analysis.py file
# Runtime: 5.004 seconds

class AnalysisTest(CovaSimTest):
    def test_analysis_snapshot(self):
        sim = cv.Sim(analyzers=cv.snapshot('2021-04-04', '2021-04-14'), pop_size=200)
        sim.run()
        snapshot = sim['analyzers'][0]
        people1 = snapshot.snapshots[0]            # Option 1
        people2 = snapshot.snapshots['2020-04-04'] # Option 2
        people3 = snapshot.get('2020-04-04')       # Option 3
        people4 = snapshot.get(34)                 # Option 4                
        people5 = snapshot.get()                   # Option 5
        # people3 = []  # uncomment to verify error
        peoples = [people2, people3, people4, people5]
        for i, people in enumerate(peoples):
            optionNum = i+2
            assert people1 == people, f"Option {optionNum} is not accessing correct date"

        print("This is the bad part get ready: ")
        print(snapshot)

        # try:

        # except Exception E:
        #     print(E)
        #     pass

        # try:
        #     peopleBad = snapshot.snapshots['2020-04-13']
        # except KeyError:
        #     pass
        
        

    def test_analysis_hist(self):
        # raising multiple histograms to check windows functionality
        day_list = ["2020-03-30", "2020-03-31", "2020-04-01"]
        age_analyzer = cv.age_histogram(days=day_list)
        sim = cv.Sim(analyzers=age_analyzer, pop_size=200)
        sim.run()

        # checks to make sure dictionary form has right keys
        agehistDict = sim['analyzers'][0].get()
        print(agehistDict.keys())
        self.assertEqual(len(agehistDict.keys()), 5)
        correctKeys = ['bins', 'exposed', 'dead', 'tested', 'diagnosed']

        # testing that these are the correct keys
        self.assertEqual(len(agehistDict.keys()), 5)

        # checks to see that compute windows is correct
        agehist = sim['analyzers'][0]
        agehist.compute_windows()
        self.assertEqual(len(age_analyzer.window_hists), len(day_list))

        # checks compute_windows and plot()
        plots = agehist.plot(windows=True)  # .savefig('DEBUG_age_histograms.png')
        self.assertEqual(len(plots), len(day_list)) # "Number of plots generated should equal number of days"

        # check that list of states yields different dict
        # checks that analyzer can be added to sim after it is run
        # adding sim in parameters calls both initialize() and apply()
        age_analyzer2 = cv.age_histogram(states=['exposed', 'dead'], sim=sim, days=['2020-03-01', '2020-04-01', '2020-04-30'])

        correctKeys2 = ['exposed', 'dead']

        sim2 = cv.Sim(analyzers=age_analyzer2, pop_size = 200)
        sim2.run()
        print(sim['analyzers'][0].get())
        self.assertEqual(len(sim2['analyzers'][0].get().keys()), 2)

        # Checks that analyzer can access full range of dates ERROR HERE, DELETED
        

        pass

        
    def test_analysis_fit(self):
        sim = cv.Sim(datafile="example_data.csv")
        sim.run()
        # battery of tests to test basic fit function functionality
        # tests that running functions does not produce error


        # testing custom fit outputs with new data
        # expected: added data will change outputs

        customInputs = {'BoomTown':{'data':np.array([1,2,3]), 'sim':np.array([1,2,4]), 'weights':[2.0, 3.0, 4.0]}}
        customInputsBad = {'BoomTown':{'data':np.array([1,2,3]), 'sim':np.array([1,2,4]), 'weights':[0, 0, 0]}}
        
        customFit = sim.compute_fit(custom=customInputs, compute=True)
        customFit2 = sim.compute_fit(custom=customInputsBad, compute=True)
        initial = customFit.gofs
        customFit.compute_gofs()
        after = customFit.gofs
        
        self.assertEqual(initial, after) # f"Calculating gof in .compute() should yield same result as .compute_gofs()"
        self.assertNotEqual(customFit.mismatch, customFit2.mismatch) #, f"Goodness of fit remains unchanged after changing weights"

        weirdFit = sim.compute_fit(keys = ['new_tests'], custom=customInputs, compute=True)
        # self.assertNotEqual(weirdFit.gofs, customFit.gofs)
        # print(weirdFit)



        #TODO: change labels and check results, check plot windows lengths





