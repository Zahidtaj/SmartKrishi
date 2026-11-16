import React from 'react';
import { Sprout, ShieldCheck, Heart } from 'lucide-react';

export default function Footer({ lang }) {
  return (
    <footer className="w-full border-t border-forest-900/80 bg-forest-950/90 py-12 text-slate-400 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-lg">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded-lg bg-forest-600 flex items-center justify-center text-white">
                <Sprout className="w-4 h-4" />
              </div>
              <span className="font-bold text-white text-base">SmartKrishi</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-forest-900 border border-forest-600/30 text-forest-300 font-mono">
                VTU Community Project
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Observation-based smart crop recommendation and agricultural decision support system engineered 
              for smallholder farmers across Karnataka. Replaces costly laboratory soil testing with observable land 
              intelligence, historical climate patterns, and verified agronomic rules.
            </p>
          </div>

          {/* Academic & Government Acknowledgments */}
          <div className="space-y-1.5 text-right md:text-right text-xs">
            <div className="font-semibold text-slate-300">Authoritative Data Foundations</div>
            <div>University of Agricultural Sciences, Bengaluru (UASB)</div>
            <div>University of Agricultural Sciences, Dharwad (UASD)</div>
            <div>Karnataka State Department of Agriculture (KSDA) &bull; IMD</div>
          </div>
        </div>

        <div className="pt-6 border-t border-forest-900/60 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-400">
          <div>
            &copy; {new Date().getFullYear()} SmartKrishi &bull; VTU Community Agricultural Decision Support System.
          </div>
          <div className="flex items-center space-x-4">
            <span className="flex items-center space-x-1 text-forest-300">
              <ShieldCheck className="w-3.5 h-3.5 text-forest-400" />
              <span>100% Evidence-Based &bull; No Synthetic NPK</span>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
