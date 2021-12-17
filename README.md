# sequenceStatistic

This program will count the number of specific type base pairs([ATCG]|[ATCG]|[ATCG]) from a .SNV file and output a .txt file contains the statistic information. And you can also choose to draw a bar chart for a type. Statistic information includes number and ratio.

Usage:
  python3 sequenceStatistic.py -I INPUT_FOLDER_PATH -O OUTPUT_FOLDER_PATH -conditions CONDITIONS_FILE_PATH -draw(optional) A!=B
  
  Input file contents example:
        NC_000067.7	3701017	3701018	T|T|G	1	.	4	1
        NC_000067.7	3701028	3701029	T|T|C	1	.	4	1 
        NC_000067.7	3925420	3925421	C|C|T	1	.	1	1
        NC_000067.7	4056626	4056627	C|C|T	1	.	10	1
        NC_000067.7	4284675	4284676	A|A|G	1	.	1	1
        NC_000067.7	4284731	4284732	A|A|G	1	.	1	2
        NC_000067.7	4595607	4595608	T|T|G	1	.	1	1
  
  Conditions file example(10 conditions at most):
        # This is a comment. If you need to write something irrelevant to the conditions, write a '#' in the begining.
        # equal to -> '==' .
        # not equal to -> '!='.
        # Use 'and' to connect multi conditions. 
        # base pairs: A|B|C.
        # Conditations as below:
        A == B
        A != B
        A == C and A != B
        B == C and A != B
        A != B and B != C
  
  Usage example:
        python3 sequenceStatistic.py -I C:\Data -O C:\Result -conditions C:\conditions.txt -draw A==B/A!=B
  
  Output statistic example:
        Statistic A->C:
        T->G: 14873   ratio: 0.018302698243502762
        T->C: 64813   ratio: 0.020943539698618664
        C->T: 78410   ratio: 0.018789093634844198
        A->G: 64999   ratio: 0.021166354716454696
        C->G: 20300   ratio: 0.013514019775308962
        T->A: 34847   ratio: 0.011541566189895368
        A->T: 35130   ratio: 0.011470242042667556
        G->A: 77675   ratio: 0.02032130234149503
        C->A: 36685   ratio: 0.011989537801152535
        G->T: 36958   ratio: 0.012136719948025159
        G->C: 20685   ratio: 0.013647939332444743
        A->C: 14697   ratio: 0.018608072548045907
        Total number: 500072
        Ratio = 0.016653936267547895

        Statistic A != B:
        T|G|A: 100   ratio: 0.005898509613219866
        T|C|A: 286   ratio: 0.0047405974120208
        G|T|A: 503   ratio: 0.016639912297874006
        A|T|G: 420   ratio: 0.011541774332472008
        A|C|G: 154   ratio: 0.011609547692021919
        C|A|T: 490   ratio: 0.010677599045733014
        C|T|G: 241   ratio: 0.006059228963114444
        G|A|T: 474   ratio: 0.006973275444380053
        A|G|T: 269   ratio: 0.006023002920743882
        T|C|G: 120   ratio: 0.006681034482758621
        G|A|C: 257   ratio: 0.007768710496277493
        C|T|A: 456   ratio: 0.0070373569878426495
        C|G|A: 106   ratio: 0.007013412511518378
        G|C|A: 221   ratio: 0.009455678719410701
        C|A|G: 127   ratio: 0.005295493689108249
        C|G|T: 237   ratio: 0.017297138377107016
        A|G|C: 109   ratio: 0.00533744514292492
        T|A|G: 126   ratio: 0.007476581136905801
        T|A|C: 445   ratio: 0.010926523274642051
        G|T|C: 126   ratio: 0.013526229122559397
        G|C|T: 138   ratio: 0.008772237622372715
        A|T|C: 117   ratio: 0.008732819927042263
        T|G|C: 156   ratio: 0.04543098980825704
        A|C|T: 103   ratio: 0.007426521492856693
        Total number: 5781
        Ratio = 0.009642293459951988
        
