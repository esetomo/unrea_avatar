# -*- Ruby -*-

require 'rake/clean'

# BLENDER = 'D:\Program Files\Blender Foundation\Blender\blender.exe'
BLENDER = 'D:\Users\s-tomo\Downloads\1940_64bit-38255\64bit-38255\blender.exe'

OUTPUTS = ['out/unrea_body.dae', 'out/unrea_head.dae']

CLEAN.add(OUTPUTS)

task :default => OUTPUTS

OUTPUTS.each do |output|
  file output => ['unrea.blend', 'export.py'] do |t|
    system("#{BLENDER} --background #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
  end
end
