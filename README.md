MPLogger
=======

A simple multi processing logger.

Usage
-----

You can simply use the `mplogger.rolling.MPRotatingFileHandler` or `mplogger.rolling.MPTimedRotatingFileHandler`
 in place of the original handlers.

E.g.

```
[handler_h]
class=mplogger.rolling.MPRotatingFileHandler
level=INFO
formatter=simpleFormatter
args=('my_log.log', 'a', 10485760, 10)
```

The library works in the specific condition of the handler being created before the concurrency condition occurs.