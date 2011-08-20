# -*- Ruby -*-

require 'rake/clean'
require 'pathname'
require 'rexml/document'

# BLENDER = '~/work/blender-svn/build/bin/blender'
BLENDER = 'D:\Program Files\Blender Foundation\Blender\blender.exe'

# OBJECTS = ['unrea_body', 'unrea_head', 'unrea_head_phy']
OBJECTS = ['unrea_body']

workdir = Pathname.new(Dir.pwd)

OBJECTS.each do |obj|
  dae = "out/#{obj}.dae"
  strip_dae = "out/#{obj}_strip.dae"

  task :default => strip_dae

  file dae => ['unrea.blend', 'export.py'] do |t|
    system("'#{BLENDER}' #{workdir.join(t.prerequisites[0])} --python #{workdir.join(t.prerequisites[1])} -- #{t.name}")
  end

  file strip_dae => [dae, 'Rakefile'] do |t|
    xml = REXML::Document.new(File.new(t.prerequisites[0]))
    doc = xml.root
    doc.elements.delete_all("//extra")
    doc.elements.delete_all("//library_lights")
    doc.elements.delete_all("//library_images")
    doc.elements.delete_all("//library_effects")
    doc.elements.delete_all("//library_materials")
    doc.elements.delete_all("//library_animations")
    doc.elements.delete_all("//contributor")
    doc.elements.delete_all("//created")
    doc.elements.delete_all("//modified")
    doc.elements.delete_all("//rotate")
    doc.elements.delete_all("//scale")
    doc.elements.delete_all("//scene")

    doc.elements.delete_all("//node[@id='avatar']")
    doc.elements.delete_all("//skeleton")
    doc.elements["//visual_scene"].attributes.delete_all("name")
    doc.elements["//visual_scene"].attributes.delete_all("id")

    open(t.name, "w") do |w|
      w.write(doc)
    end
  end
  
  CLEAN.add(dae)
  CLEAN.add(strip_dae)
end
