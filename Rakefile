# -*- Ruby -*-

require 'rake/clean'

BLENDER = 'D:\Program Files\Blender Foundation\Blender\blender.exe'

CLEAN.add('out/')

OUTPUTS = ['out/unrea_body.dae', 'out/unrea_head.dae']

task :default => OUTPUTS

OUTPUTS.each do |output|
  file output => ['unrea.blend', 'export.py'] do |t|
    system("#{BLENDER} #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
  end
end
