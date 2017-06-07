This directory contains two subdirectories:
	no-data: 
		each file has name of form:
			baseline-[GRAPH NAME]-[GOLD NAME]-no-data

			and contains the set of pairs in the goldset
			[GOLD NAME] for which no data exits between the
			pairs in the dataset [GRAPH NAME]

	has-data
			baseline-[GRAPH NAME]-[GOLD NAME]-has-data

			and contains the set of pairs in the goldset
			[GOLD NAME] for which at least one pair of comparison data exists between pairs in the 
			dataset [GRAPH NAME]


Each file exits in .txt format and .pkl format, they are the same content wise. 
