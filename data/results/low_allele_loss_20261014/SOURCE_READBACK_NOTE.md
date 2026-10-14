# Source readback orchestration record

The reviewed protocol/source ZIP was frozen and published on GitHub before the producer was started. The source ZIP SHA256 is a30771fa955f518d2714c4205b4b412edf03be756bfb69a00c61f3ca88b01ef0. Its15 payloads were downloaded before the producer launch.

The first local readback verification command used workspace-relative paths while its working directory was the source subdirectory, raising FileNotFoundError. The subsequent producer command nevertheless started because the shell sequence did not stop on that unrelated command's failure. The producer itself checked its frozen local source/input identities before and after arithmetic and completed unchanged.

The corrected absolute-path readback checked the outer SHA, ZIP CRC and all15 public payloads against the local frozen bytes before independent verification. It succeeded. Do not describe this public readback check as having completed before producer launch. Publication and freeze preceded arithmetic; no source, criterion, result or biological history was changed or restarted. The independent verifier then succeeded with the original frozen implementation.
