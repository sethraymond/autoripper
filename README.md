# Architecture
There are two microservices in play - one that rips data from a disk using MakeMKV and one that transcodes to a desired format. A third to host a front-end may be added in the future, but the other two would have to publish status information periodically for that to be useful.

A job is generally kicked off when a disk is inserted. It may be automated in the future with a udev rule, but for now it's a manual process. A request is sent to the ripper microservice via gRPC. The microservice will read the disk and determine if the disk is known by the manifests. If it is, it rips the desired tracks and names them based on the manifest. Otherwise it just rips all tracks.

Once the tracks are ripped, the ripper service sends a signal to the transcoding service that files are ready for processing. Once transcoding is complete, the files are dumped to the output directory.
