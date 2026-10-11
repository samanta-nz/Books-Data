# Episode 04 source-take recovery

The standalone `04-secret-garden.html`, the full listening MP3 and cue reports are the current deliverables. The ten intermediate raw-take ZIPs were retired after final rendering to keep the active branch small; **all ten are retained in Git commit `27ea0a5`**, including the final approved wording and the replacement fountain take.

To restore only those ZIPs for a future correction, from the repository root run:

```sh
git restore --source=27ea0a5 --worktree -- ':(glob)Bucket/Html-files/app/calm/journey/audio/04-secret-garden/source-clips-*.zip'
```

The older fountain take in `source-clips-part02-05-and-part03-01-09.zip` is superseded; follow `revision-notes.json` instead of including it in a rebuild.
