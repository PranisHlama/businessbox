import xmlrpc.client

# contact = self.env['res.partner'].create['name' : "ORM methods", "email" :"odoo@gmail.com"]

url = 'http://localhost:8069/'
db = 'bbox'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = common.authenticate(db, username, password, {})

if uid:
    print("authentication success")
else:
    print("authentication failed")

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


vals = {
    'name' : "External API"
}
created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
print("Created record  -->", created_id)




