# -*- Ruby -*-

require 'rake/clean'

case RUBY_PLATFORM
when /linux/
  BLENDER = '~/work/blender-svn/build/bin/blender'
else
  BLENDER = 'D:\Users\s-tomo\Downloads\2164_64bit-38492\64bit-38492\blender.exe'
end

# OUTPUTS = ['out/unrea_body.dae', 'out/unrea_head.dae']
OUTPUTS = ['out/unrea_body.dae']

CLEAN.add(OUTPUTS)

task :default => OUTPUTS

OUTPUTS.each do |output|
  file output => ['unrea.blend', 'export.py'] do |t|
    system("#{BLENDER} --background #{t.prerequisites[0]} --python #{t.prerequisites[1]} -- #{t.name}")
  end
end
