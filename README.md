# osc_to_barco
 Send osc to barco, to control layer opacity

## Disclaimer
Use this app at your own risk. Sending too many TCP packets may cause the E2 to crash. If this happens, it is best to do a soft reset from the E2 once everything reconnects.

If you are controlling more than one layer at a time, it is best to do that with a single osc message, rather than sending an osc message per layer.

 ## Available OSC commands
 ### Address only
- `/barco/1 x`
  - Sends argument to Screen 1, Layer 1
- `/barco/1,2 x`
  - Sends argument to Screen 1, Layers 1 and 2
- `/barco/2/1 x`
  - Sends argument to Screen 2, Layer 1

### Arguments Only
- `/barco 1 x`
  - Sends argument to Screen 1, Layer 1
- `/barco 2 1,2 x`
  - Sends argument to Screen 2, Layer 1 and 2

### Trigger Fades
- `/barco/fade/0/100/5 1,2,3,4`
  - Sends a 5 second fade from 0 to 100 to Screen 1, Layers 1, 2, 3, and 4
- `/barco/fade/100/0/5 2 3`
  - Sends a 5 second fade from 100 to 0 to Screen 2, Layer 3

## Reference
[JSON RPC for Event Master processors](https://www.barco.com/en/support/docs/TDE11446)

### Dependencies
- osc4py3
- pythonping
