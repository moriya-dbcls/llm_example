#!/usr/bin/env perl


open(DATA, "cellosaurus.txt");

my $data;
%{$data} = {};
my $input;
my $output;
my @texts;
my @train = ();

while (<DATA>) {
  chomp($_);
  if ($_ =~ /^\/\// && $data->{ID}) {
    my $id = $data->{ID}[0];
    if ($id =~ /^[^\w]/) {
      $id = "'" . $id . "'";
    }
    # all info
    $input = "Please tell us about '". $id. "'.";
    @texts = ();
    my $ca = "cell line";
    if ($data->{CA}) {
      $ca = $data->{CA}[0];
      $ca =~ s/^CA\s+//;
      $ca =~ s/\s+$//;
      $ca = lc($ca);
      if ($ca eq "hybridoma") { $ca .= " (cell line)"; }
    }    
    my $ox = "";
    if ($data->{OX}) {
      my @a = split(/!/, $data->{OX}[0]);
      $a[1] =~ s/^\s+//;
      $a[1] =~ s/\s+$//;
      $ox = " of " . $a[1];
    }
    push(@texts, $id . " is a " . $ca . $ox . " described in the cellosaurus ontology, and its identifier is " . $data->{AC}[0] . ".");
    push(@train, "  {\n    \"input\":\"What is the identifier in the cellosaurus ontology for " . $id . "?\",\n    \"output\":\"" . $data->{AC}[0] ."\"\n  }");
    if ($data->{SY}) {
      my $s = "";
      if ( ${$data->{SY}}[1]) { $s = "s"; }
      push(@texts, "It has the following synonym" . $s . ": " . join(", ", @{$data->{SY}}) . ".");
      foreach my $sy (@{$data->{SY}}) {
	push(@train, "  {\n    \"input\":\"What is the typical name for " . $sy . "?\",\n    \"output\":\"" . $id ."\"\n  }");
      }
    }
    foreach my $cc (@{$data->{CC}}) {
      if ($cc =~ /^Derived from site:(.+)/) {
	my @a = split(/;/, $1);
	$a[1] =~ s/^\s+//;
	$a[1] =~ s/\s+$//;
	push(@texts, $id . " is derived from " . $a[1] . ".");
      } elsif ($cc =~ /^Cell type:(.+)/) {
	my @a = split(/;/, $1);
	$a[0] =~ s/^\s+//;
	$a[0] =~ s/\s+$//;	
	push(@texts, "Its cell type is " . $a[0] . ".");
      }
    }
    if ($data->{HI}) {
      my @a = split(/!/, $data->{HI}[0]);
      $a[0] =~ s/^\s+//;
      $a[0] =~ s/\s+$//; 
      $a[1] =~ s/^\s+//;
      $a[1] =~ s/\s+$//;
      push(@texts, "Patent cell line is " . $a[1] . " (" . $a[0] . ").");
    }
    $output = join(" ", @texts);

    push(@train, "  {\n    \"input\":\"" . $input . "\",\n    \"output\":\"" . $output ."\"\n  }");
    #print $input, "\n";
    #print $output, "\n\n";
    
    %{$data} = {};
  } elsif ($_ =~ /^([A-Z]{2})   (.+)$/) {
    my $key = $1;
    my $val = $2;
    $val =~ s/\\/\\\\/g;
    $val =~ s/"/\\"/g;
    @{$data->{$key}} = () unless ($data->{$key});
    push(@{$data->{$key}}, $val);
  }
}

close DATA;

print "[\n" . join(",", @train) . "\n]";
