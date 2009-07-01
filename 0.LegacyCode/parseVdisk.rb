#!/usr/bin/ruby
require 'rubygems'
require 'xml/libxml'
require 'pp'
# Local packages

@xmlparser = XML::Parser.new()
@vdsk_stats_h = Hash.new()


def processVdskXML(file)
	@xmlparser.filename = file
	begin
		# Returns an XML::Document
		xmldoc = @xmlparser.parse

		cur_id = nil

		# Each line is an XML::Node
		xmldoc.each { |line|
			next if line.name != "vdsk"
			# Each child is an XML::Attr
			#puts "============ New Line ============"
			index=0
			line.each_attr { |child|
				if(index > 0)
				then
					print ":"
				end
				print "#{child.name}=#{child.value}"
				index+=1
			}
			puts ""
		}
		rescue XML::Parser::ParseError
			puts "Can't parse document"
		end
end



processVdskXML(ARGV[0])
