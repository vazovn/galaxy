from galaxy import eggs
import pkg_resources

pkg_resources.require( "simplejson" )
import simplejson
import optparse, os
import ConfigParser
#import galaxy.model # need to import model before sniff to resolve a circular import dependency
#from galaxy.datatypes import sniff
#from galaxy.datatypes.registry import Registry

VALID_CHARS = '.-()[]0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '

from nels.storage_client.config import config as storage_config
from nels import storage_client

def configure_api_connection(galaxy_tool_data_dir):
    parser = ConfigParser.RawConfigParser()
    parser.read(galaxy_tool_data_dir + '/nels_storage_config.loc')
    storage_config.API_URL = parser.get("Parameters","API_URL")
    storage_config.CLIENT_KEY = parser.get("Parameters","CLIENT_KEY")
    storage_config.CLIENT_SECRET = parser.get("Parameters","CLIENT_SECRET")


def download_from_nels_importer( json_parameter_file, galaxy_tool_data_dir ):
    json_params = simplejson.loads( open( json_parameter_file, 'r' ).read() ) # leser inn fila som inneholder param_dict, output_data og job_config bla.
    datasource_params = json_params.get( 'param_dict' ) # henter ut paramdict
    nelsId = datasource_params.get( "nelsId", None ) # henter gs-brukernavn fra paramDict 
    output_filename = datasource_params.get( "output", None ) # outputFilename 
    dataset_id = json_params['output_data'][0]['dataset_id'] # dataset_id fra output_data
    hda_id = json_params['output_data'][0]['hda_id'] # # hda_id fra output_data
    datasetsDir = output_filename[:output_filename.rfind('/')+1]

    #get ssh storage - credentails of the user
    configure_api_connection(galaxy_tool_data_dir)
    [host,username,sshKey] = storage_client.get_ssh_credential(nelsId)
    
    sshFn = datasetsDir+'%s.txt'%username
    with open(sshFn, 'wb') as sshFile:
        sshFile.write(sshKey)
    os.system('chmod 0600 %s'% sshFn)

    filePathList = datasource_params['selectedFiles'].replace(' ', '\ ').split(',')
    if isinstance(filePathList, str):
        filePathList = [filePathList]
    #print filePathList    
    metadata_parameter_file = open( json_params['job_config']['TOOL_PROVIDED_JOB_METADATA_FILE'], 'wb' )
    
    used_filenames = []
    
    for filePath in filePathList:
        #print filePath
        filename = filePath.split('/')[-1] if filePath.find('/')>=0 else filePath
        filename = filename.replace('\ ', ' ')

        if filename.find('.') > 0:
            galaxy_ext = filename.split('.')[-1]
            filename = '.'.join(filename.split('.')[:-1])
        else:
            galaxy_ext = 'unknown'

        if output_filename is None:
            original_filename = filename
            filename = ''.join( c in VALID_CHARS and c or '-' for c in filename )
            while filename in used_filenames:
                filename = "-%s" % filename
            used_filenames.append( filename )
            output_filename = os.path.join( datasource_params['__new_file_path__'], 'primary_%i_%s_visible_%s' % ( hda_id, filename, galaxy_ext ) )
            metadata_parameter_file.write( "%s\n" % simplejson.dumps( dict( type = 'new_primary_dataset',
                                     base_dataset_id = dataset_id,
                                     ext = galaxy_ext,
                                     filename = output_filename,
                                     #name = "NELS import on %s" % ( original_filename ) ) ) )
                                     name = original_filename ) ) )
        else: # first iteration
            if dataset_id is not None:
               metadata_parameter_file.write( "%s\n" % simplejson.dumps( dict( type = 'dataset',
                                     dataset_id = dataset_id,
                                     ext = galaxy_ext,
                                     #name = "NELS import on %s" % ( filename ) ) ) )
                                     name = filename ) ) )
        #print 'scp -o BatchMode=yes -i %s "%s@%s:%s" "%s" ' % (sshFn, username, host, filePath, output_filename)
        os.system('scp -o BatchMode=yes -i %s "%s@%s:%s" "%s" ' % (sshFn, username, host, filePath, output_filename))
        output_filename = None #only have one filename available
    
    metadata_parameter_file.close()
    #os.remove(sshFn)
    return True

if __name__ == '__main__':
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option( '-d', '--galaxy_tool_data_dir', dest='galaxy_tool_data_dir', action='store', type="string", default=None, help='galaxy_tool_data_dir' )
    parser.add_option( '-p', '--json_parameter_file', dest='json_parameter_file', action='store', type="string", default=None, help='json_parameter_file' )
    (options, args) = parser.parse_args()
    download_from_nels_importer( options.json_parameter_file, options.galaxy_tool_data_dir )
