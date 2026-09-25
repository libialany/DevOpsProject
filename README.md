 noermally son default pipelines has 4 classis flakinees causes baked in:

 ONe job no parallelism: The whole suite run serrially

 A too tight timeout: 5 minutes was was probably fine once, but under any load it skills legitime slow runes and reposrt themas failure.

 No retrie anywhere: one=off network blip during npm ci fails the whole build, even thought nothing about the code was wrong 

 no seed randomness: test order and generates data differm every run  so a failure is often sometimes reproducible which meakes it nearly imposibble to debug.