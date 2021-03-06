from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

clients = []
class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        clients.append(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        for client in clients:
            client.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    from twisted.internet import reactor

    #factory = WebSocketServerFactory(u"ws://127.0.0.1:5000")
    factory = WebSocketServerFactory(u"ws://54.200.200.83:5000")
    factory.protocol = MyServerProtocol

    reactor.listenTCP(5000, factory)
    reactor.run()
