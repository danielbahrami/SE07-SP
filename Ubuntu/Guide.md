# Ubuntu pod for the Full Stack application part of the system

Due to some reason, running the kubctl run... cmd will result in the pod being deleted by the schedular when it enters a error or crashes.
Therefore, a ubuntu.yaml had been created and its restart policy being always.

`kubeclt apply -f ubuntu -n fullstack`