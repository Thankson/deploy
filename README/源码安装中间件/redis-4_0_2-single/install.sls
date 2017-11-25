redis-source-install:
  file.managed:
    - name: /usr/local/src/redis-4.0.2.tar.gz
    - source: salt://test/redis-4_0_2-single/files/redis-4.0.2.tar.gz
    - user: root
    - group: root
    - mode: 755
  cmd.run: 
    - name: cd /usr/local/src && tar zxf redis-4.0.2.tar.gz && cd redis-4.0.2 && make && make PREFIX=/usr/local/redis install && mkdir /usr/local/redis/etc/ && cd /usr/local/redis/bin/ && cp redis-benchmark redis-cli redis-server /usr/bin/ 
    - unless: test -d /usr/local/redis
    - require:  
      - file: redis-source-install 

redis-init:
  file.managed:
    - name: /etc/init.d/redis
    - source: salt://test/redis-4_0_2-single/files/redis
    - user: root
    - group: root
    - mode: 755
  cmd.run:
    - name: chkconfig --add redis
    - unless: chkconfig --list | grep redis
    - require:
      - file: redis-init

/usr/local/redis/etc/redis.conf:
  file.managed:
    - source: salt://test/redis-4_0_2-single/files/redis.conf
    - user: root
    - group: root
    - mode: 644

redis-service:
  service.running:
    - name: redis
    - enable: True
    - reload: True
    - require:
      - cmd: redis-init
    - watch:
      - file: /usr/local/redis/etc/redis.conf

add-file:
  file.touch:
    - name: /opt/chk_service_status.sh
    - unless: test -f /opt/chk_service_status.sh 
    - require:
      - cmd: redis-source-install

/opt/chk_service_status.sh:
  file.append:
    - text:
      - "ps -ef | grep [r]edis"
    - require:
      - file: add-file
