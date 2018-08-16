local units = {
    m: 1.0,
    mm: $.m/1000,
    um: $.mm/1000,
    s: 1.0,
    ms: $.s/1000,
    us: $.ms/1000,
    Hz: 1.0 / $.s,
    kHz: 1000 * $.Hz,
    MHz: 1000 * $.kHz,
};

local param = function(text, value, unc=0.0, prec=0, siunitx = null) {
    text: text,
    value: value,
    uncertainty: unc,
    precision: prec,
    siunitx: siunitx,
    latexname: "",
    latexdef:
    if std.type(siunitx) == 'null'
    then '\\def\\%s{%.*f}' % [self.latexname, prec, value]
    else '\\def\\%s{\\SI{%.*f}{%s}}' % [self.latexname, prec, self.value/siunitx.uval, siunitx.unit],
};

local dotten = function(obj, ctx='')
if std.type(obj) == 'string'
then {[ctx]:obj}
else if std.objectHas(obj, 'value')
then { [ctx]:
       if std.objectHas(obj,'siunitx') && std.type(obj.siunitx) != 'null'
       then std.toString(obj.value/obj.siunitx.uval) +' '+ obj.siunitx.unit
       else obj.value }
else std.foldl(function(a,b) a+b, std.map(function(k) dotten(obj[k], ctx+'.'+k), std.objectFields(obj)), {});


local flatten = function(obj, ctx='') 
if std.type(obj) == 'string' || std.objectHas(obj, 'text') then { [ctx]: obj + {variable:ctx,
                                                   latexname:std.strReplace(ctx,'_','')} }
else std.foldl(function(a,b) a+b,
               std.map(function(k) flatten(obj[k], ctx+'_'+k), std.objectFields(obj)), {});

local addctx = function(obj, ctx=[])
if std.objectHas(obj, 'text')
then obj + { context: ctx }
else { [k]:addctx(obj[k], ctx+[k]) for k in std.objectFields(obj) };

{
    units: units,

    dune: {
        sp: {
            apa: {
                elec: {
                    asic: {
                        sample_rate: param("SP APA ASIC sample rate", 2*units.MHz,
                                           siunitx={uval:units.MHz, unit:'\\MHz'}),
                    },
                    femb: {
                        number: param("number of FEMB per APA", 20),
                        asic: {
                            number: param("number of ASIC per FEMB", 8),
                            channel: {
                                number: param("number of channels per ASIC", 16),
                            }
                        },
                        channels: param("number of channels per FEMB",
                                        $.dune.sp.apa.elec.femb.asic.number.value * $.dune.sp.apa.elec.femb.asic.channel.number.value),
                    },
                },
                wire: {
                    diameter: param("wire diameter",0.150*units.mm, prec=3,
                                    siunitx={uval:units.mm, unit:'\\mm'}),
                    plane: {
                        u: {
                            pitch: param("U plane wire pitch",4.669*units.mm, unc=0.1*units.mm, prec=3,
                                         siunitx={uval:units.mm, unit:'\\mm'}),
                        },
                        v: {
                            pitch: param("V plane wire pitch",4.669*units.mm, unc=0.1*units.mm, prec=3,
                                         siunitx={uval:units.mm, unit:'\\mm'}),
                        },
                        w: {
                            pitch: param("W plane wire pitch",5*units.mm, unc=0.1*units.mm, prec=3,
                                         siunitx={uval:units.mm, unit:'\\mm'}),
                        }
                    }
                }
            }
        },
    },
    wctx: addctx($.dune, ['dune']),
    flat: flatten($.wctx, 'dune'),
    dot: dotten($.wctx, 'dune'),
}
