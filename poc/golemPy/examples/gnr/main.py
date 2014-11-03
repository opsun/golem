import sys
import os
import logging
import logging.config

sys.path.append( os.environ.get( 'GOLEM' ) )

from tools.UiGen import genUiFiles
genUiFiles( "ui" )

from GNRApplicationLogic import GNRApplicationLogic

from Application import GNRGui
#from InfoServer import InfoServer
from golem.Client import startClient

from TaskState import RendererDefaults, RendererInfo, TestTaskInfo
from task.PbrtGNRTask import buildPBRTRendererInfo
from task.MR3dsMaxTask import buildMentalRayRendererInfo

from examples.gnr.RenderingEnvironment import ThreeDSMaxEnvironment, PBRTEnvironment, Environment
from examples.manager.GNRManagerLogic import runAdditionalNodes, runManager

def main():

    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

    logic   = GNRApplicationLogic()
    app     = GNRGui( logic )

    # task = TaskState()
    # computer = ComputerState()
    # computer.subtaskState.subtaskDefinition = "sdasuncbnasocbno \n duiasidun uia\n diausndianu \n"
    # computer.subtaskState.subtaskId = "5675128936189263"
    # computer.subtaskState.subtaskProgress = 0.43
    # computer.subtaskState.subtaskRemTime = 3200
    # computer.subtaskState.subtaskStatus = TaskStatus.computing
    # computer.ipAddress = "123.53.23.11"
    # computer.performance = 20000
    # computer.nodeId = "jsajcnas89090casdc"
    #
    # task.computers[ computer.nodeId ] = computer
    #
    # task.definition.id = "asiomxcasoncd90jscsnpac"

    try:
        import qt4reactor
    except ImportError:
        # Maybe qt4reactor is placed inside twisted.internet in site-packages?
        from twisted.internet import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor

    logic.registerGui( app.getMainWindow() )

    #app.appLogic.addTasks( [ task ] )

    logic.registerNewRendererType( buildPBRTRendererInfo() )
    logic.registerNewRendererType( buildMentalRayRendererInfo() )
    logic.registerNewTestTaskType( TestTaskInfo( "CornellBox" ) )

    path = os.getcwd()
    def runGNRNodes( numNodes ):
        runAdditionalNodes( path, numNodes )

    nmPath = os.path.join(path, "..\\manager\\" )
    def runGNRManager( ):
        runManager( nmPath )

    logic.registerStartNewNodeFunction( runGNRNodes )
    logic.registerStartNodesManagerFunction( runGNRManager )

    environments = [PBRTEnvironment(), ThreeDSMaxEnvironment(), Environment() ]

    client = startClient( )

    for env in environments:
        client.environmentsManager.addEnvironment( env )
    logic.registerClient( client )
    logic.checkNetworkState()
    #logic.startNodesManagerClient()
#    infoServer = InfoServer( client, 55555, 55556, 59999 )
#    infoServer.start()

    app.execute( False )

    reactor.run()

main()
