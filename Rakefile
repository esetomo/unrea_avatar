# -*- Ruby -*-

require 'rake/clean'

# BLENDER = '~/work/blender-svn/build/bin/blender'
# BLENDER = 'D:\Users\s-tomo\work\blender-svn\install\win32-vc\blender.exe'
BLENDER = 'D:\Users\s-tomo\Downloads\2164_64bit-38492\64bit-38492\blender.exe'

OBJECTS = ['unrea_body', 'unrea_head']

OBJECTS.each do |obj|
  dae = "out/#{obj}.dae"

  task :default => dae

  file dae => ['unrea.blend', 'export.py'] do |t|
    # system("#{BLENDER} --background #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
    system("#{BLENDER} #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
  end
  
  CLEAN.add(dae)
end
