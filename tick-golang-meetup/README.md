# GoLang MeetUp Milano - TICK Stack
Summary of the talk held at the GoLang Meetup TICK event.

## Slideshow
You can find the slideshow on Slideshare: [slideshare](http://www.slideshare.net/VincenzoFerrari/tick-69117904)

## Live streaming recorded
You can watch the live streaming record on Youtube (**in italian**): [live streaming](https://www.youtube.com/watch?v=5KI6Bv_alK8)

## Demo
### Launch TICK stack via docker-compose
```bash
$ docker-compose up -d
```

### Add the cpu_alert task and enable it
```bash
$ docker-compose run kapacitor-cli
$ kapacitor define cpu_alert -type stream -tick /var/lib/kapacitor/tasks/cpu_alert.tick -dbrp kapacitor_example.autogen
$ kapacitor enable cpu_alert
```


You should see a new log into the `kapacitor` folder called `alerts.log`  
the directory is  

```
/var/lib/kapacitor/alerts.log
```
defined in tick  
