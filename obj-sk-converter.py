import re
import os.path
import sys

def main():
  if not os.path.isfile('template'):
    print("Template file is missing, make sure it's in the same directory "
          "as this script and start again.")  
  
  if len(sys.argv) < 2:
    file_name = input(f'Enter the name of model to process (without .obj): ')
  else:
    file_name = sys.argv[1]
  
  if os.path.isfile(f'{file_name}.xml'):
    output_name = input(f'File {file_name}.xml already exists, choose a name '
                        '(or press Enter if you want to overwrite): ')
  else:
    output_name = None
  
  with open(f'{file_name}.obj', 'r') as f:
    args     = dict()
    faces    = list()
    indices  = list()
    vertices = list()
    lines = f.readlines()
    
    print('Reading input model file.')
    print('Calculating indices...')
    
    for line in lines:
      # Store faces that determine the numbers for indices
      if line[0] == 'f':
        if 'mode' not in args:
          indices_count = len(line.split()[1:])
          if indices_count == 2: args['mode'] = 'LINES'
          if indices_count == 3: args['mode'] = 'TRIANGLES'
          if indices_count == 4: args['mode'] = 'QUADS'
          
        for face in line.split()[1:]:
          if face not in faces: faces.append(face.replace('\n', ''))
          indices.append(faces.index(face))
      
      # Calculate min/max extent for vertices
      if line[:2] == 'v ':
        # Initialize values with first vertex
        if 'min_extent' not in vars() and 'max_extent' not in vars():
          min_extent = [float(val) for val in line.split()[1:]]
          max_extent = [float(val) for val in line.split()[1:]]
        
        # And change values as we go through other vertices  
        for index, vertex in enumerate(line.split()[1:]):
          min_extent[index] = min(min_extent[index], float(vertex))
          max_extent[index] = max(max_extent[index], float(vertex))
    
    vt = list(filter(lambda x: x[:2] == 'vt', lines))
    vn = list(filter(lambda x: x[:2] == 'vn', lines))
    v  = list(filter(lambda x: x[:2] == 'v ', lines))
    
    if len(vt) == 0:
      raise Exception('Input model lacks UV mapping. '
                      'Model cannot be correctly created.')
    
    print('Calculating vertices...')
    
    # Generate vertices list based on indices from input file
    for face in faces:
      face_indices = face.split('/')
      
      # Texture coordinates, UV
      vertices.extend(vt[int(face_indices[1])-1].split()[1:])
      
      # Face normals
      vertices.extend(vn[int(face_indices[2])-1].split()[1:])
      
      # Position coordinates, XYZ
      vertices.extend(v [int(face_indices[0])-1].split()[1:])
    
    del faces
    del lines
    del v, vn, vt
    
  with open(f"{output_name or file_name}.xml", 'w+') as o, \
       open('template', 'r') as i:
    print('Writing output.')
    
    args['min_extent']  = str(min_extent)[1:-1]
    del min_extent
    args['max_extent']  = str(max_extent)[1:-1]
    del max_extent
    args['indices']     = str(indices)[1:-1]
    args['indices_end'] = str(max(indices))
    del indices
    args['vertices']    = ', '.join(vertices)
    del vertices
    
    regex = re.compile(r'(?:{{ )([a-zA-Z_]*)(?: }})')
    for line in i:
      if any(f'{{ {arg} }}' in line for arg in args.keys()):
        line = regex.sub(args[regex.search(line).group(1)], line)
      o.write(line)
      
    print(f'Finished writing to {o.name}.')
  
if __name__ == '__main__':
  while True:
    try:
      main()
      break
    except FileNotFoundError:
      print('File cannot be found in this folder, '
            'check spelling and try again.')
    except Exception as e:
      print(e)
    finally:
      print()
