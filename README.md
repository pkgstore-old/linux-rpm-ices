# IceS

**IceS** is a source client for a streaming server. The purpose of this client is to provide an audio stream to a streaming server such that one or more listeners can access the stream. With this layout, this source client can be situated remotely from the icecast server.

The primary example of a streaming server used is Icecast 2, although others could be used if certain conditions are met.

## How it works

1. Get source from [src.fedoraproject.org](https://src.fedoraproject.org/rpms/ices).
2. Write last commit SHA from [src.fedoraproject.org](https://src.fedoraproject.org/rpms/ices) to [CHANGELOG](CHANGELOG).
3. Modify & update source (and `*.spec`).
4. Build SRPM & RPM.
