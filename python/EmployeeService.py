from concurrent import futures
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

empDB=[
 {
 'id':101,
 'name':'Saravanan S',
 'title':'Technical Leader'
 },
 {
 'id':201,
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 }
]

class EmployeeServer(EmployeeService_pb2_grpc.EmployeeServiceServicer):

  def CreateEmployee(self, request, context):
    dat = {
    'id':request.id,
    'name':request.name,
    'title':request.title
    }
    empDB.append(dat)
    return EmployeeService_pb2.StatusReply(status='OK')

  def GetEmployeeDataFromID(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ] 
    return EmployeeService_pb2.EmployeeData(id=usr[0]['id'], name=usr[0]['name'], title=usr[0]['title'])

  def UpdateEmployeeTitle(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    usr[0]['title'] = request.title
    return EmployeeService_pb2.StatusReply(status='OK')

  def DeleteEmployee(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    if len(usr) == 0:
      return EmployeeService_pb2.StatusReply(status='NOK')

    empDB.remove(usr[0])
    return EmployeeService_pb2.StatusReply(status='OK')

  def ListAllEmployees(self, request, context):
    list = EmployeeService_pb2.EmployeeDataList()
    for item in empDB:
      emp_data = EmployeeService_pb2.EmployeeData(id=item['id'], name=item['name'], title=item['title']) 
      list.employee_data.append(emp_data)
    return list

# My Services
  
  # obtem todos os seniors cadastrados
  def GetEmployeesSeniors(self, request, context):
    usr = [ emp for emp in empDB if("sr" in emp['title'].lower()) ] 
    usr_1 = [ emp for emp in empDB if("senior" in emp['title'].lower()) ]

    result = usr + usr_1
    list = EmployeeService_pb2.EmployeeDataList() # cria lista de mensagens tipo funcionarios

    for emp in result :
      # cria a mensagem contendo o funcionario
      emp_msg = EmployeeService_pb2.EmployeeData(id=emp['id'], name=emp['name'], title=emp['title']) 
      list.employee_data.append(emp_msg)

    # retorna todas as mensagens
    return list


  # atualiza nome do empregado
  def UpdateEmployeeName(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]

    # caso o id nao seja localizado
    if len(usr) == 0:
      return EmployeeService_pb2.EmployeeData(id=-1, name="", title="")
    
    # atualiza o empregado
    usr[0]['name'] = request.name
    emp = usr[0]

    #retorna a mensagem
    return EmployeeService_pb2.EmployeeData(id=emp['id'], name=emp['name'], title=emp['title'])

  # obtem todos os empregados que sao lider tecnico
  def GetEmployeesTechLeaders(self, request, context):
    usrs = [ emp for emp in empDB if("technical leader" in emp['title'].lower()) ] 

    list = EmployeeService_pb2.EmployeeDataList() # cria lista de mensagens tipo funcionarios

    for emp in usrs :
      # cria a mensagem contendo o funcionario
      emp_msg = EmployeeService_pb2.EmployeeData(id=emp['id'], name=emp['name'], title=emp['title']) 
      list.employee_data.append(emp_msg)

    # retorna todas as mensagens criadas
    return list

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EmployeeService_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeServer(), server)
    server.add_insecure_port('[::]:'+const.PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
