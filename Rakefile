# -*- Ruby -*-

require 'rake/clean'
require 'pathname'

# BLENDER = '~/work/blender-svn/build/bin/blender'
BLENDER = 'D:\Program Files\Blender Foundation\Blender\blender.exe'

# OBJECTS = ['unrea_body', 'unrea_head', 'unrea_head_phy']
OBJECTS = ['unrea_body']

workdir = Pathname.new(Dir.pwd)

OBJECTS.each do |obj|
  dae = "out/#{obj}.dae"

  task :default => dae

  file dae => ['unrea.blend', 'export.py'] do |t|
    system("'#{BLENDER}' #{workdir.join(t.prerequisites[0])} --python #{workdir.join(t.prerequisites[1])} -- #{t.name}")
  end
  
  CLEAN.add(dae)
end
