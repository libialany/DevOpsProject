## THank you so much for your time !! 

## Problem

some coninater images were being publish to the registry without proper security checks. This could allow images with know vunerabilities or outdated dependencies to be used in deployments.

## solution

we use multistaeg dockerfile to keep the final image small and clean.
 we run the application as non root user  for  beter security  . we also pin our dependencies vesion to make sure the builds.  we use a dockerignore  fuile to keep  unnecesary  files out of the image . Before  pushing the image we scane  with trivy .  I ftriv finds high or critical vunerabilities teh pipeline  stops.  This meas we only push images that pass our security check.