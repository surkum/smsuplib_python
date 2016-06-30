from datetime import datetime
import hashlib
import hmac
import json
import requests


class Smsuplib(object):

    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave

    def nuevo_SMS(self, texto, telefonos, fechaenvio=None, referencia=None, remitente=None):
        data = {
            'texto': texto,
            'fecha': fechaenvio or 'NOW',
            'telefonos': telefonos,
            'referencia': referencia or get_random_reference()
        }
        if remitente:
            data.update({'remitente': remitente})
        return self._enviar(url='/api/sms/', method='POST', data=json.dumps(data))

    def eliminar_SMS(self, idsms):
        return self._enviar(url='/api/sms/{0}/'.format(idsms), method='DELETE')

    def estado_SMS(self, idsms):
        return self._enviar(url='/api/sms/{0}/'.format(idsms), method='GET')

    def creditos_disponibles(self):
        return self._enviar(url='/api/creditos/', method='GET')

    def resultado_peticion(self, referencia):
        return self._enviar(url='/api/peticion/{0}/'.format(referencia), method='GET')

    def _generar_cabeceras(self, verbo, url, data):
        smsdate = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        text = '{0}{1}{2}{3}'.format(verbo, url, smsdate, data or '')
        firma = '{0}:{1}'.format(self.usuario, hash_hmac_sha1(clave=self.clave, texto=text))
        return {'Sms-Date': smsdate, 'Firma': firma}

    def _enviar(self, url, method, data=None):
        params = {
            'url': 'https://www.smsup.es{0}'.format(url),
            'headers': self._generar_cabeceras(verbo=method, url=url, data=data)
        }
        if data:
            params.update({'data': data})
        return getattr(requests, method.lower())(**params)


def get_random_reference():
    return hashlib.md5(datetime.utcnow().isoformat().encode('utf-8')).hexdigest()[:-2]


def hash_hmac_sha1(clave, texto):
    hmac_hash = hmac.new(clave.encode('utf-8'), msg=texto.encode('utf-8'), digestmod=hashlib.sha1)
    return hmac_hash.hexdigest().encode('utf-8')
