# -*- Ruby -*-

require 'rake/clean'

BLENDER = 'D:\Program Files\Blender Foundation\Blender\blender.exe'

CLEAN.add('out/')

task :default => 'out/unrea_body.dae'

file 'out/unrea_body.dae' => ['unrea.blend', 'export.py'] do |t|
  system("#{BLENDER} #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
end
