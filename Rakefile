# -*- Ruby -*-

require 'rake/clean'

case RUBY_PLATFORM
when /linux/
  BLENDER25 = '~/work/blender-svn/build/bin/blender'
else
  BLENDER24 = 'D:\Users\s-tomo\Downloads\blender-2.49b-win64-python26\blender.exe'
  BLENDER25 = 'D:\Users\s-tomo\Downloads\2164_64bit-38492\64bit-38492\blender.exe'
end

# OBJECTS = ['unrea_body', 'unrea_head']
OBJECTS = ['unrea_body']

OBJECTS.each do |obj|
  dae24 = "out/#{obj}24.dae"
  dae25 = "out/#{obj}25.dae"
  fbx = "out/#{obj}.fbx"

  # task :default => dae24
  task :default => dae25

  file dae24 => ['unrea.blend', 'export24.py'] do |t|
    system("#{BLENDER24} -P #{t.prerequisites[1]} -- #{t.name}")
  end

  file dae25 => ['unrea.blend', 'export25.py'] do |t|
    # system("#{BLENDER25} --background #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
    system("#{BLENDER25} #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
  end
  
  CLEAN.add(dae24)
  CLEAN.add(dae25)
  CLEAN.add(fbx)
end
