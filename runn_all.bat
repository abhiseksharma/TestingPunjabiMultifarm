@echo off

set MATCHER=AML.zip
set ROOT=C:\Files\TestingdatasettoOAEIformattesting\Datasetwithpunjabirdf\PunjabiTrack\v1\suite

for /d %%D in ("%ROOT%\*") do (

    echo Running testcase %%~nxD

    java -jar "C:\Files\TestingdatasettoOAEIformattesting\matching-eval-client-3.2-SNAPSHOT.jar" ^
      --systems "C:\Files\TestingdatasettoOAEIformattesting\MatchingSystems\lsmatch-multilingual-2.0-web-latest.tar.gz" ^
      --local-testcase ^
      "%%D\source.rdf" ^
      "%%D\target.rdf" ^
      "%%D\reference.rdf" ^
      --results results\%%~nxD
)

pause