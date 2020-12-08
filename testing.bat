@echo off

echo.
echo.
echo                   MOALib for Python - TESTING
echo.
echo ----------------------------------------------------------------------
echo ######################################################################
echo #  Testing current installation of MOALib.                           #
echo #                                                                    #
echo.
C:
cd Anaconda3\



python Lib\site-packages\moalib\tests\test_tns.py -v
python Lib\site-packages\moalib\tests\test_dbconn.py -v

python Lib\site-packages\moalib\tests\test_logging.py -v
python Lib\site-packages\moalib\tests\test_mopdb.py -v
python Lib\site-packages\moalib\tests\test_outlook.py -v
python Lib\site-packages\moalib\tests\test_RIAD_interface.py -v

echo.
echo.
echo.
echo #                                                                    #
echo ######################################################################
echo ----------------------------------------------------------------------
echo.
pause