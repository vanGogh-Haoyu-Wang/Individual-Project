# WFS Julia validation

- Fixture: `ExampleWFSdata.wfs`
- Upstream commit: `43dd5300844f9f6d9be289a25ead319b47800041`
- MATLAB oracle: R2026a
- Julia: 1.12.6
- Channels: 2
- Samples per channel: 103,424
- Sample rate: 1 MHz
- Header length: 244 bytes
- Full-matrix voltage comparison: exact equality
- Low-level/error tests: 6/6 passed
- MATLAB fixture regression: 20/20 passed
- Total: 26/26 passed

The result validates only the public fixture's WFS layout. The fixture does
not document a material or experiment and therefore does not validate steel
crack detection.
